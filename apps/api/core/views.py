from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Fest, Item, ItemRule
from .serializers import FestSerializer, FestCreateSerializer, FestDetailSerializer, ItemCreateSerializer, ItemSerializer, ItemRuleCreateSerializer, ItemRuleSerializer
from .permissions import IsAuthority

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

@api_view(["POST"]) 
@permission_classes([IsAuthenticated, IsAuthority])
def fest_create(request):
	serializer = FestCreateSerializer(data=request.data, context={"request": request})
	if serializer.is_valid():
		fest = serializer.save()
		return Response(FestSerializer(fest).data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def fest_detail(request, fest_id: int):
	fest = get_object_or_404(Fest.objects.prefetch_related("items__rules", "rules"), pk=fest_id, is_published=True)
	data = FestDetailSerializer(fest).data
	return Response(data)

@api_view(["POST"]) 
@permission_classes([IsAuthenticated, IsAuthority])
def fest_item_create(request, fest_id: int):
	fest = get_object_or_404(Fest, pk=fest_id)
	serializer = ItemCreateSerializer(data=request.data)
	if serializer.is_valid():
		item = Item.objects.create(fest=fest, **serializer.validated_data)
		return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"]) 
@permission_classes([IsAuthenticated, IsAuthority])
def item_rule_create(request, item_id: int):
	item = get_object_or_404(Item, pk=item_id)
	serializer = ItemRuleCreateSerializer(data=request.data)
	if serializer.is_valid():
		rule = ItemRule.objects.create(item=item, fest=item.fest, **serializer.validated_data)
		return Response(ItemRuleSerializer(rule).data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"]) 
@permission_classes([IsAuthenticated, IsAuthority])
def fest_rule_create(request, fest_id: int):
	fest = get_object_or_404(Fest, pk=fest_id)
	serializer = ItemRuleCreateSerializer(data=request.data)
	if serializer.is_valid():
		rule = ItemRule.objects.create(fest=fest, text=serializer.validated_data["text"]) 
		return Response(ItemRuleSerializer(rule).data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def fest_ask(request, fest_id: int):
	fest = get_object_or_404(Fest.objects.prefetch_related("items__rules", "rules"), pk=fest_id)
	question = request.data.get("question", "")
	context_parts = [fest.name, fest.description or ""]
	for r in fest.rules.all():
		context_parts.append(r.text)
	for it in fest.items.all():
		context_parts.append(it.title)
		context_parts.append(it.description or "")
		for r in it.rules.all():
			context_parts.append(r.text)
	context_text = "\n".join([p for p in context_parts if p])
	if init_chat_model and HumanMessage and question:
		try:
			model = init_chat_model()
			prompt = f"Based only on this information, answer the question.\n\nCONTEXT:\n{context_text}\n\nQUESTION: {question}"
			result = model.invoke([HumanMessage(content=prompt)])
			content = getattr(result, "content", None)
			if isinstance(content, str) and content:
				return Response({"answer": content})
		except Exception:
			pass
	return Response({"answer": "No model configured. Read the rules and items above."})

@api_view(["POST"])
def item_ask(request, item_id: int):
	item = get_object_or_404(Item.objects.prefetch_related("rules", "fest__rules"), pk=item_id)
	question = request.data.get("question", "")
	context_parts = [item.fest.name, item.title, item.description or ""]
	for r in item.fest.rules.all():
		context_parts.append(r.text)
	for r in item.rules.all():
		context_parts.append(r.text)
	context_text = "\n".join([p for p in context_parts if p])
	if init_chat_model and HumanMessage and question:
		try:
			model = init_chat_model()
			prompt = f"Based only on this information, answer the question.\n\nCONTEXT:\n{context_text}\n\nQUESTION: {question}"
			result = model.invoke([HumanMessage(content=prompt)])
			content = getattr(result, "content", None)
			if isinstance(content, str) and content:
				return Response({"answer": content})
		except Exception:
			pass
	return Response({"answer": "No model configured. Read the rules above."})
