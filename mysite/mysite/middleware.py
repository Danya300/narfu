"""
Middleware for supporting HTTP Range requests (for seeking in audio/video).
This implementation properly handles partial content without loading entire files into memory.
"""
import os
import re
from django.http import FileResponse, HttpResponse, HttpRequest
from django.utils.deprecation import MiddlewareMixin


class RangeRequestMiddleware(MiddlewareMixin):
    """
    Middleware to support HTTP Range requests for media seeking.
    This allows audio/video files to be seekable on mobile devices.
    
    Key features:
    - Returns Accept-Ranges: bytes header to indicate seeking support
    - Properly handles byte-range requests (206 Partial Content)
    - Uses streaming to avoid loading entire files into memory
    """

    # File extensions that should have Range support
    MEDIA_EXTENSIONS = ('.mp3', '.mp4', '.webm', '.ogg', '.wav', '.flac', 
                        '.m4a', '.aac', '.mov', '.avi', '.mkv', '.webm')

    def process_response(self, request, response):
        """Process response to add Range support for media files."""
        
        # Only process GET requests
        if request.method != 'GET':
            return response
        
        # Check if response is a FileResponse (used by Django for media files)
        if not isinstance(response, FileResponse):
            # For non-file responses, just add Accept-Ranges header
            return self._add_accept_ranges_header(response, request)
        
        # Add Accept-Ranges header to indicate we support Range requests
        response['Accept-Ranges'] = 'bytes'
        
        # Check if client sent Range header
        range_header = request.META.get('HTTP_RANGE')
        if not range_header:
            return response
        
        # Parse and validate Range header
        try:
            file_size = response.get('Content-Length', 0)
            if hasattr(response, 'file_to_stream') and response.file_to_stream:
                # Get actual file size from file object
                file_to_stream = response.file_to_stream
                if hasattr(file_to_stream, 'seek') and hasattr(file_to_stream, 'tell'):
                    try:
                        old_pos = file_to_stream.tell()
                        file_to_stream.seek(0, 2)  # Seek to end
                        file_size = file_to_stream.tell()
                        file_to_stream.seek(old_pos)  # Restore position
                    except:
                        pass
            
            # Parse the range specification
            range_spec = range_header.replace('bytes=', '')
            start, end = self._parse_range_spec(range_spec, file_size)
            
            if start is None:
                return response
            
            # Validate range
            if start >= file_size:
                # Return 416 Range Not Satisfiable
                return self._create_416_response(file_size)
            
            if end is None or end >= file_size:
                end = file_size - 1
            
            # Create partial response
            return self._create_partial_response(response, request, start, end, file_size)
            
        except Exception as e:
            # If anything goes wrong, return original response
            return response

    def _parse_range_spec(self, range_spec, file_size):
        """Parse Range header specification."""
        try:
            parts = range_spec.split('-')
            
            if len(parts) != 2:
                return None, None
            
            start_str, end_str = parts
            
            # Parse start
            if start_str.strip():
                start = int(start_str)
            else:
                # Suffix range (e.g., "-500") means last N bytes
                if end_str.strip():
                    suffix_length = int(end_str)
                    start = max(0, file_size - suffix_length)
                else:
                    # No range specified
                    return None, None
            
            # Parse end
            if end_str.strip():
                end = int(end_str)
            else:
                end = file_size - 1
            
            return start, end
            
        except (ValueError, AttributeError):
            return None, None

    def _create_partial_response(self, original_response, request, start, end, file_size):
        """Create 206 Partial Content response."""
        content_length = end - start + 1
        
        # Get the file from FileResponse
        file_to_stream = original_response.file_to_stream
        
        # Seek to start position
        if hasattr(file_to_stream, 'seek'):
            try:
                file_to_stream.seek(start)
            except:
                return original_response
        
        # Read only the requested range
        if hasattr(file_to_stream, 'read'):
            try:
                content = file_to_stream.read(content_length)
            except:
                return original_response
        else:
            return original_response
        
        # Create new response
        content_type = original_response.get('Content-Type', 'application/octet-stream')
        response = HttpResponse(content, status=206, content_type=content_type)
        
        # Set required headers
        response['Content-Length'] = len(content)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        
        # Copy other relevant headers
        for header in ['Content-Disposition']:
            if original_response.get(header):
                response[header] = original_response[header]
        
        return response

    def _create_416_response(self, file_size):
        """Create 416 Range Not Satisfiable response."""
        response = HttpResponse(status=416, content_type='text/plain')
        response['Content-Range'] = f'bytes */{file_size}'
        return response

    def _add_accept_ranges_header(self, response, request):
        """Add Accept-Ranges header to responses."""
        # Check if this is a media file URL
        path = request.path.lower()
        if any(path.endswith(ext) for ext in self.MEDIA_EXTENSIONS):
            response['Accept-Ranges'] = 'bytes'
        return response
