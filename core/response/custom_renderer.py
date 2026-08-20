from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        # Already wrapped by CustomPagination / success_response
        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        status_code = getattr(response, "status_code", 200)
        success = 200 <= status_code < 400

        wrapped = {
            "success": success,
            "message": "Success" if success else "Error",
            "data": data if success else None,
            "errors": None if success else data,
        }
        return super().render(wrapped, accepted_media_type, renderer_context)
