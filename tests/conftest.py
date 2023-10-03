from pytest_regtest2 import register_converter_pre, register_converter_post


@register_converter_pre
def result(txt):
    return txt


@register_converter_post
def result(txt):
    return txt.upper()
