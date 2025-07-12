import language_tool_python as lang
from textblob import TextBlob as text
def spell_correct(query):
    return str(text(query).correct())
def grammar_correct(query):
    tool = lang.LanguageTool('en-US')
    matches = tool.check(query)
    corrected_query = lang.utils.correct(query, matches)
    return corrected_query

def correction(query):
    corrected_query = spell_correct(query)
    corrected_query = grammar_correct(corrected_query)
    return corrected_query
