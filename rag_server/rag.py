from embed import restore_db
from dotenv import load_dotenv
import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from langchain_community.chat_message_histories import SQLChatMessageHistory

DB_PATH = "sqlite:///chat_history.db"

# Load environment variables from .env
load_dotenv()
llm_api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize model
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    api_key=llm_api_key,  
)

def format_md():
    md = (
        MarkdownIt('commonmark', {'breaks':True,'html':True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable('table')
    )
    return md

""" 
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

 """

def get_session_history(session_id: str):
    """Return a persistent ChatMessageHistory for a session."""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DB_PATH
    )

def get_full_history(session_id: str):
    """Return the full chat history (as list of dicts) for a given session."""
    history = get_session_history(session_id)
    messages = history.messages  # returns a list of Message objects
    result = []

    for msg in messages:
        # Message type can be HumanMessage, AIMessage, SystemMessage, etc.
        role = "human" if msg.type == "human" else "ai"
        result.append({"role": role, "content": msg.content})

    return result

def format_chat_history(history):
    """Return simple readable string for UI."""
    lines = []
    for msg in history:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "human":
            lines.append(f"🧑 You: {content}")
        elif role == "ai":
            lines.append(f"🤖 AI: {content}")
    return "\n".join(lines)

store = {}
chain = None

def format_context(context_list):
    """
    Cleans and formats LangChain Document context output.

    Args:
        context_list (list): List of langchain Document objects or dicts.

    Returns:
        str: Formatted string like "doc1.pdf: pages 1, 2; doc2.pdf: pages 3"
    """
    try:
        doc_pages = {}

        for doc in context_list:
            # Handle both Document objects and dicts
            if hasattr(doc, "metadata"):
                meta = doc.metadata
            elif isinstance(doc, dict):
                meta = doc.get("metadata", {})
            else:
                continue

            source = meta.get("source")
            page = meta.get("page")

            if not source:
                continue

            doc_name = os.path.basename(source)
            doc_pages.setdefault(doc_name, set())

            if isinstance(page, int):
                doc_pages[doc_name].add(page)

        if not doc_pages:
            return "No context found."

        # Sort pages and build formatted string
        formatted = "; ".join(
            f"{doc}: pages {', '.join(map(str, sorted(pages)))}"
            for doc, pages in doc_pages.items()
        )

        return formatted

    except Exception as e:
        return f"Error formatting context: {e}"
    

# --- RAG CHAIN ---
def build_rag_chain():
    qdrant = restore_db()
    retriever = qdrant.as_retriever()

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", (
                "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question which can be understood "
                "without the chat history."
            )),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following context to answer concisely. "
        "If you don't know, say you don't know.\n\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )


# create on-demand
def ask_rag(question: str, session_id: str = "default"):
    global chain
    if not chain:
        chain = build_rag_chain()

    result = chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}},
    )

    context = format_context(result.get("context", []))
    md = format_md()
    html_text = md.render(result["answer"])
    full_history = get_full_history(session_id)
    full_history_formatted = format_chat_history(full_history)

    return html_text, context, full_history_formatted
