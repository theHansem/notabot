from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from uuid import uuid4
from telegram.utils.helpers import escape_markdown

#def inline_caps(update, context):
#    query = update.inline_query.query
#    if not query:
#        return
#    results = list()
#    results.append(
#        InlineQueryResultArticle(
#            id=query.upper(),
#            title='Caps',
#            input_message_content=InputTextMessageContent(query.upper())
#        )
#    )
#    context.bot.answer_inline_query(update.inline_query.id, results)


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    if query == "":
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]
    update.inline_query.answer(results)
