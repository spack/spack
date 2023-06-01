# The name of the Pygments (syntax highlighting) style to use.
# We use our own extension of the default style with a few modifications
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Comment, Generic, Text


class SpackStyle(DefaultStyle):
    styles = DefaultStyle.styles.copy()
    background_color = "#f4f4f8"
    styles[Generic.Output] = "#355"
    styles[Generic.Prompt] = "bold #346ec9"
