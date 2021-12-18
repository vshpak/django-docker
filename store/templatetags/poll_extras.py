from django import template
import pymorphy2

register = template.Library()


def get_case(count, gender):
    # gender = neut || masc || femn
    count %= 100
    if 5 <= count <= 20:
        return {"gent", "plur"}
    count %= 10
    if count == 1:
        return {"nomn", "sing"}
    if 2 <= count <= 4:
        if gender == "masc":
            return {"gent", "sing"}
        else:
            return {"accs", "plur"}
    return {"gent", "plur"}


@register.simple_tag
def change_case(value, case, plural=False):
    morph = pymorphy2.MorphAnalyzer(lang="ru")
    params = {case, "plur" if plural else "sing"}
    return morph.parse(value)[0].inflect(params).word.lower()


@register.simple_tag
def define_plural_and_change(value, count=0):
    morph = pymorphy2.MorphAnalyzer(lang="ru")
    genger = str(morph.parse(value)[0].tag).split(",")[2].split(" ")[0]
    params = get_case(count, genger)
    return morph.parse(value)[0].inflect(params).word.lower()
