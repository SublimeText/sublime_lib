from sphinx.transforms import SphinxTransform
import sphinx.addnodes as SphinxNodes


SPECIAL_METHODS = {
    '__getitem__': '{self}[{0}]',
    '__setitem__': '{self}[{0}] = {1}',
    '__delitem__': 'del {self}[{0}]',
    '__contains__': '{0} in {self}',

    '__lt__': '{self} < {0}',
    '__le__': '{self} <= {0}',
    '__eq__': '{self} == {0}',
    '__ne__': '{self} != {0}',
    '__gt__': '{self} > {0}',
    '__ge__': '{self} >= {0}',

    '__hash__': 'hash({self})',
    '__len__': 'len({self})',

    '__add__': '{self} + {0}',
    '__sub__': '{self} - {0}',
    '__mul__': '{self} * {0}',
    '__matmul__': '{self} @ {0}',
    '__truediv__': '{self} / {0}',
    '__floordiv__': '{self} // {0}',
    '__mod__': '{self} % {0}',
    '__divmod__': 'divmod({self}, {0})',
    '__pow__': '{self} ** {0}',
    '__lshift__': '{self} << {0}',
    '__rshift__': '{self} >> {0}',
    '__and__': '{self} & {0}',
    '__xor__': '{self} ^ {0}',
    '__or__': '{self} | {0}',

    '__neg__': '-{self}',
    '__pos__': '+{self}',
    '__abs__': 'abs({self})',
    '__invert__': '~{self}',
}


class PrettifySpecialMethods(SphinxTransform):
    default_priority = 800

    def apply(self):
        methods = (
            sig for sig in self.document.traverse(SphinxNodes.desc_signature)
            if 'class' in sig
        )

        for ref in methods:
            name_node = ref.next_node(SphinxNodes.desc_name)
            method_name = name_node.astext()

            if method_name in SPECIAL_METHODS:
                param_names = [p.astext() for p in ref.traverse(SphinxNodes.desc_parameter)]

                ref.remove(ref.next_node(SphinxNodes.desc_parameterlist))

                name_node.replace_self(
                    SphinxNodes.desc_name(
                        name_node.source,
                        SPECIAL_METHODS[method_name].format(*param_names, self='d'),
                        **name_node.attributes
                    )
                )


def show_special_methods(app, what, name, obj, skip, options):
    if what == 'class' and name in SPECIAL_METHODS:
        return False
