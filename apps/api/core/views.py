from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Fest
from .serializers import FestSerializer

try:
    from langchain.schema import HumanMessage
    from langchain.chat_models import init_chat_model
except Exception:
    HumanMessage = None
    init_chat_model = None


@api_view(["POST"])
def echo(request):
    text = request.data.get("text", "")

    reply = f"Echo: {text}".strip()
    if init_chat_model and HumanMessage and text:
        try:
            model = init_chat_model()
            result = model.invoke([HumanMessage(content=f"Repeat: {text}")])
            content = getattr(result, "content", None)
            if isinstance(content, str) and content:
                reply = content
        except Exception:
            pass

    return Response({"reply": reply}, status=status.HTTP_200_OK)

@api_view(["GET"])
def fest_list(request):
    qs = Fest.objects.filter(is_published=True).order_by("-starts_at", "name")
    data = FestSerializer(qs, many=True).data
    return Response({"results": data}, status=status.HTTP_200_OK)
