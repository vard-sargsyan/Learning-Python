import pandas as pd
import copy


"""
Each operation/method/function in 'operations'/'methods'/'functions' is tested for all objects supplied as arguments.
- In binary operations/methods/functions each object in 'selves' is tested as the first operand/argument or self, and
each object in 'others' being tested as the other operand/argument. Results of each operation/method/function are
aggregated into a separate dataframe to be printed into a separate sheet in an Excel file. As Excel limits the use of
certain symbols in worksheet names, for operations containing those symbols the keys should be spelled out.
- In unary operations/methods/functions all results are aggregated into a single dataframe to be printed into a single
sheet in an Excel file.

'meth/op/func_results' - > dictionary to be converted into a dataframe containing the method results
- dataframe column names / header -> dictionary keys -> objects acting as the first argument/self 
- dataframe columns -> dictionary values -> lists of operation/method/function results for each key / column name 
- dataframe row names / index
    -> objects acting as the second/other argument, if binary
    -> operations/methods/functions, if unary

To avoid messing column heads and row names due to object modification in in-place operations, the actual executions of
operations/methods/functions use deep copies of the original objects unless the deepcopy method does not work for the
given object (in this case those are only the memoryview and dictionary view objects that anyway do not change as a
result of in-place operations).

Calculation of results for each individual operation/method/function is implemented through 'eval' and 'exec' functions
to allow looping through operations and only changing the operation/method/function itself in a standard expression.

If an operation/method/function is not defined for the given operand(s)/argument(s) an Exceptionn type is returned. This
is later used to color-code the Excel sheets based on result type.
"""

bytes0 = b''
bytes1 = b'asdf'
bytes2 = b'qwerty'

bytearray0 = bytearray(bytes0)
bytearray1 = bytearray(bytes1)
bytearray2 = bytearray(bytes2)

set0 = set()
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

dict0 = {}
dict1 = {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
dict2 = {4: 16, 5: 25, 6: 36, 7: 49, 8: 64}

# default objects to be used as operands/arguments
def_objects = dict(int0=0, int1=-5, int2=-1, int3=1, int4=4,
                   bool0=False, bool1=True,
                   float0=0.0, float1=-3.0, float2=-2.5, float3=-1.0, float4=-0.25, float5=0.8, float6=1.0, float7=2.5,
                   float8=3.0,
                   complex0=0j, complex1=2 + 1j, complex2=1 - 4j, complex3=-5 - 3j, complex4=-3 + 2j, complex5=3j,
                   complex6=2 + 0j, complex7=-3j, complex8=-2 - 0j,
                   list0=[], list1=[1, 2, 3, 4, 5], list2=[4, 5, 6, 7, 8],
                   tuple0=(), tuple1=(1, 2, 3, 4, 5), tuple2=(4, 5, 6, 7, 8),
                   range0=range(0), range1=range(5), range2=range(1, 10, 2),
                   str0='', str1='asdf', str2='qwerty',
                   bytes0=bytes0, bytes1=bytes1, bytes2=bytes2,
                   bytearray0=bytearray0, bytearray1=bytearray1, bytearray2=bytearray2,
                   memoryview0=memoryview(bytes0), memoryview1=memoryview(bytes1), memoryview2=memoryview(bytearray1),
                   set0=set0, set1=set1, set2=set2,
                   frozenset0=frozenset(), frozenset1=frozenset(set1), frozenset2=frozenset(set2),
                   dict0=dict0, dict1=dict1, dict2=dict2,
                   keys0=dict0.keys(), keys1=dict1.keys(), keys2=dict2.keys(),
                   values0=dict0.values(), values1=dict1.values(), values2=dict2.values(),
                   items0=dict0.items(), items1=dict1.items(), items2=dict2.items())

def gen1(x):
    while x > 0:
        yield x + 1
        x -= 1

def gen2(x):
    while x > 0:
        yield x
        x -= 1
        
more_objs = dict(iterator1=iter(set1), iterator2=iter(bytes2), generator1=gen1(5), generator2=gen2(5),
                 enumerate1=enumerate(set1), enumerate2=enumerate(bytes2), fhandle1=open('numeric.txt'),
                 fhandle2=open('download.jpg'), type1 = int, type2=dict, function1=abs, function2=max,
                 method1=type(complex.conjugate), method2=type(str.upper))

# default operations / methods / functions (unary and binary) to be tested. Any other combination can be feeded into the functions and will work as well.
def_un_ops = {'-': '-', '+': '+', '~': '~'}

def_bin_ops = {'+': '+', 'IP_+=': '+=', '-': '-', 'IP_-=': '-=', 'mult': '*', 'IP_mult=': '*=', 'div': '/',
               'IP_div=': '/=', 'fl_div': '//', 'IP_fl_div=': '//=', '%': '%', 'IP_%=': '%=', 'pow': '**',
               'IP_pow=': '**=', '<<': '<<', 'IP_<<=': '<<=', '>>': '>>', 'IP_>>=': '>>=', '&': '&', 'IP_&=': '&=',
               '^': '^', 'IP_^=': '^=', '|': '|', 'IP_|=': '|=', 'is': 'is', '==': '==', '!=': '!=', '<': '<', '<=': '<=', '>': '>',
               '>=': '>=', 'in': 'in'}

def_funcs = {'abs': 'abs', 'all': 'all', 'any': 'any', 'ascii': 'ascii', 'bin': 'bin', 'bool': 'bool',
             'breakpoint': 'breakpoint', 'bytearray': 'bytearray', 'bytes': 'bytes', 'chr': 'chr', 'complex': 'complex',
             'delattr': 'delattr', 'dict': 'dict', 'divmod': 'divmod', 'enumerate': 'enumerate', 'float': 'float',
             'frozenset': 'frozenset', 'getattr': 'getattr', 'hasattr': 'hasattr', 'hash': 'hash', 'hex': 'hex',
             'id': 'id', 'int': 'int', 'iter': 'iter', 'len': 'len', 'list': 'list', 'max': 'max',
             'memoryview': 'memoryview', 'min': 'min', 'next': 'next', 'oct': 'oct', 'ord': 'ord', 'pow': 'pow',
             'range': 'range', 'repr': 'repr', 'reversed': 'reversed', 'round': 'round', 'set': 'set',
             'setattr': 'setattr', 'slice': 'slice', 'sorted': 'sorted', 'str': 'str', 'sum': 'sum', 'tuple': 'tuple',
             'zip': 'zip'}

def_un_magics = {'__abs__': '__abs__', '__bool__': '__bool__', '__ceil__': '__ceil__', '__dir__': '__dir__',
                 '__float__': '__float__', '__floor__': '__floor__', '__hash__': '__hash__', '__index__': '__index__',
                 '__int__': '__int__', '__invert__': '__invert__', '__iter__': '__iter__', '__len__': '__len__',
                 '__neg__': '__neg__', '__next__': '__next__', '__pos__': '__pos__', '__reduce__': '__reduce__',
                 '__repr__': '__repr__', '__reversed__': '__reversed__', '__sizeof__': '__sizeof__',
                 '__str__': '__str__', '__trunc__': '__trunc__'}

def_bin_magics = {'__add__': '__add__', '__and__': '__and__', '__contains__': '__contains__',
                  '__delitem__': '__delitem__', '__divmod__': '__divmod__', '__eq__': '__eq__',
                  '__floordiv__': '__floordiv__', '__ge__': '__ge__', '__getattribute__': '__getattribute__',
                  '__getitem__': '__getitem__', '__gt__': '__gt__', '__iadd__': '__iadd__', '__iand__': '__iand__',
                  '__imul__': '__imul__', '__ior__': '__ior__', '__isub__': '__isub__', '__ixor__': '__ixor__',
                  '__le__': '__le__', '__lshift__': '__lshift__', '__lt__': '__lt__', '__mod__': '__mod__',
                  '__mul__': '__mul__', '__ne__': '__ne__', '__or__': '__or__', '__radd__': '__radd__',
                  '__rand__': '__rand__', '__rdivmod__': '__rdivmod__', '__reduce_ex__': '__reduce_ex__',
                  '__rfloordiv__': '__rfloordiv__', '__rlshift__': '__rlshift__', '__rmod__': '__rmod__',
                  '__rmul__': '__rmul__', '__ror__': '__ror__', '__rrshift__': '__rrshift__',
                  '__rshift__': '__rshift__', '__rsub__': '__rsub__', '__rtruediv__': '__rtruediv__',
                  '__rxor__': '__rxor__', '__sub__': '__sub__', '__truediv__': '__truediv__', '__xor__': '__xor__'}

def_methods = {'add': 'add', 'append': 'append', 'as_integer_ratio': 'as_integer_ratio', 'bit_length': 'bit_length',
               'c_contiguous': 'c_contiguous', 'capitalize': 'capitalize', 'casefold': 'casefold', 'cast': 'cast',
               'center': 'center', 'clear': 'clear', 'conjugate': 'conjugate', 'contiguous': 'contiguous',
               'copy': 'copy', 'count': 'count', 'decode': 'decode', 'denominator': 'denominator',
               'difference': 'difference', 'difference_update': 'difference_update', 'discard': 'discard',
               'encode': 'encode', 'endswith': 'endswith', 'expandtabs': 'expandtabs', 'extend': 'extend',
               'f_contiguous': 'f_contiguous', 'find': 'find', 'format': 'format', 'format_map': 'format_map',
               'from_bytes': 'from_bytes', 'fromhex': 'fromhex', 'fromkeys': 'fromkeys', 'get': 'get', 'hex': 'hex',
               'imag': 'imag', 'index': 'index', 'insert': 'insert', 'intersection': 'intersection',
               'intersection_update': 'intersection_update', 'is_integer': 'is_integer', 'isalnum': 'isalnum',
               'isalpha': 'isalpha', 'isascii': 'isascii', 'isdecimal': 'isdecimal', 'isdigit': 'isdigit',
               'isdisjoint': 'isdisjoint', 'isidentifier': 'isidentifier', 'islower': 'islower',
               'isnumeric': 'isnumeric', 'isprintable': 'isprintable', 'isspace': 'isspace', 'issubset': 'issubset',
               'issuperset': 'issuperset', 'istitle': 'istitle', 'isupper': 'isupper', 'items': 'items',
               'itemsize': 'itemsize', 'join': 'join', 'keys': 'keys', 'ljust': 'ljust', 'lower': 'lower',
               'lstrip': 'lstrip', 'maketrans': 'maketrans', 'nbytes': 'nbytes', 'ndim': 'ndim',
               'numerator': 'numerator', 'obj': 'obj', 'partition': 'partition', 'pop': 'pop', 'popitem': 'popitem',
               'readonly': 'readonly', 'real': 'real', 'release': 'release', 'remove': 'remove', 'replace': 'replace',
               'reverse': 'reverse', 'rfind': 'rfind', 'rindex': 'rindex', 'rjust': 'rjust', 'rpartition': 'rpartition',
               'M_rsplit': 'rsplit', 'rstrip': 'rstrip', 'setdefault': 'setdefault', 'shape': 'shape', 'sort': 'sort',
               'split': 'split', 'splitlines': 'splitlines', 'start': 'start', 'startswith': 'startswith',
               'step': 'step', 'stop': 'stop', 'strides': 'strides', 'strip': 'strip', 'suboffsets': 'suboffsets',
               'swapcase': 'swapcase', 'symmetric_difference': 'symmetric_difference',
               'symmetric_difference_update': 'symmetric_difference_update', 'title': 'title', 'to_bytes': 'to_bytes',
               'tobytes': 'tobytes', 'tolist': 'tolist', 'toreadonly': 'toreadonly', 'translate': 'translate',
               'union': 'union', 'update': 'update', 'upper': 'upper', 'values': 'values', 'zfill': 'zfill'}


# HELPER FUNCTIONS
def try_deep_copy(obj):
    try:
        copy_obj = copy.deepcopy(obj)
    except:
        copy_obj = obj
    return copy_obj

# Trying to evalualte an expression. If an exception occurs, it means the given operation / method / function
# is not supported for the given operand(s)/argument(s)
def try_eval(expression, copy_self_, copy_other=None):
    try:
        executed = eval(expression)  # calculating the result by executing eval on a standard expression
    except:
        executed = Exception()
    return executed

# Trying to execute a code containing in-place operation. If an exception occurs, it means the given operation
# is not supported for the given operand(s)/argument(s)
def try_exec_eval(statement, expression, copy_self_, copy_other=None):
    try:
        ldic = locals()
        exec(statement, globals(), ldic)
        copy_self_ = ldic['copy_self_']
        copy_other = ldic['copy_other']
        executed = eval(expression)
    except:
        executed = Exception()
    return executed

# Round floats and and parts of complex numbers.
def custom_round(obj):
    if type(obj) is float:
        return round(obj, 2)
    elif type(obj) is complex:
        return complex(round(obj.real, 2), round(obj.imag, 2))
    else:
        return obj

# CORE TEST FUNCTIONS

# Unary operations
def unary_ops_test(objects=def_objects, operations=def_un_ops, OUTPUT_FILE='Unary_operations.xlsx'):
    op_results = {'Operation': [operation for operation in operations]}

    for self_ in objects:
        col_head = f'{objects[self_]}\n{type(objects[self_])})'
        self_results = []  # list of results in the column 'self_'

        for operation in operations:
            eval_str = f'{operations[operation]}copy_self_'
            copy_self_ = try_deep_copy(objects[self_])
            result = try_eval(eval_str, copy_self_)  # calculating the result by executing eval on a standard expression
            result = custom_round(result)
            self_results.append(f'{result}\n{type(result)}')
        op_results[col_head] = self_results

    pd.DataFrame(op_results).to_excel(OUTPUT_FILE, sheet_name='Unary_operations', index=False, freeze_panes=(1, 1))

# Binary operations
def binary_ops_test(selves=def_objects, others=def_objects, operations=def_bin_ops,
                    OUTPUT_FILE='Binary_operations.xlsx'):
    # To ensure proper execution keys of in-place operators should start with "IP_"

    all_results = {}  # dictionary object with operations as keys and respective dataframes as values.

    for operation in operations:
        exec_str = 'pass'
        if operation.startswith('IP_'):
            exec_str = f'copy_self_ {operations[operation]} copy_other'
            eval_str = 'copy_self_'
        else:
            eval_str = f'copy_self_ {operations[operation]} copy_other'

        op_results = {'Other': [f'{others[other]}\n{type(others[other])}' for other in others]}

        for self_ in selves:
            col_head = f'{selves[self_]}\n{type(selves[self_])})'
            self_results = []  # list of results in the column 'self_'
            for other in others:
                copy_self_ = try_deep_copy(selves[self_])
                copy_other = try_deep_copy(others[other])
                result = try_exec_eval(exec_str, eval_str, copy_self_, copy_other)
                result = custom_round(result)
                self_results.append(f'{result}\n{type(result)}')
            op_results[col_head] = self_results

        all_results[operation] = pd.DataFrame(op_results)

    writer = pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='w')  # a writer object to write multiple sheets
    workbook = writer.book

    for operation in all_results:
        try:
            workbook.remove(workbook[operation])
        except:
            pass
        all_results[operation].to_excel(writer, sheet_name=operation, index=False, freeze_panes=(1, 1))

    writer.save()

# unary methods (methods only requiring self as an argument)
def unary_meth_test(objects=def_objects, methods=def_methods, OUTPUT_FILE='Unary_methods.xlsx'):
    meth_results = {'Method': [method for method in methods]}

    for self_ in objects:
        col_head = f'{objects[self_]}\n{type(objects[self_])})'
        self_results = []  # list of results in the column 'self_'

        for method in methods:
            eval_str = f'copy_self_.{methods[method]}()'
            copy_self_ = try_deep_copy(objects[self_])
            result = try_eval(eval_str, copy_self_)  # calculating the result by executing eval on a standard expression
            result = custom_round(result)
            self_results.append(f'{result}\n{type(result)}')
        meth_results[col_head] = self_results

    pd.DataFrame(meth_results).to_excel(OUTPUT_FILE, sheet_name='Unary_methods', index=False, freeze_panes=(1, 1))

# binary methods (requiring another argument in addition to self)
def binary_meth_test(selves=def_objects, others=def_objects, methods=def_methods, OUTPUT_FILE='Binary_methods.xlsx'):
    all_results = {}  # dictionary object with methods as keys and respective dataframes as values.

    for method in methods:

        eval_str = f'copy_self_.{methods[method]}(copy_other)'

        meth_results = {'Other': [f'{others[other]}\n{type(others[other])}' for other in others]}

        for self_ in selves:
            col_head = f'{selves[self_]}\n{type(selves[self_])})'
            self_results = []  # list of results in the column 'self'
            for other in others:
                copy_self_ = try_deep_copy(selves[self_])
                copy_other = try_deep_copy(others[other])
                result = try_eval(eval_str, copy_self_, copy_other)  # calculating the result by executing eval on a standard expression
                result = custom_round(result)
                self_results.append(f'{result}\n{type(result)}')
            meth_results[col_head] = self_results

        all_results[method] = pd.DataFrame(meth_results)

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='w') as writer:  # a writer object to write multiple sheets
        workbook = writer.book
    
        for method in all_results:
            try:
                workbook.remove(workbook[method])
            except:
                pass
            all_results[method].to_excel(writer, sheet_name=method, index=False, freeze_panes=(1, 1))
    
        writer.save()

# unary functions (functions only requiring one argument)
def unary_func_test(objects=def_objects, functions=def_funcs, OUTPUT_FILE='Unary_functions.xlsx'):
    func_results = {'Function': [function for function in functions]}

    for self_ in objects:
        col_head = f'{objects[self_]}\n{type(objects[self_])})'
        self_results = []  # list of results in the column 'self_'

        for function in functions:
            eval_str = f'{functions[function]}(copy_self_)'
            copy_self_ = try_deep_copy(objects[self_])
            result = try_eval(eval_str, copy_self_)  # calculating the result by executing eval on a standard expression
            result = custom_round(result)
            self_results.append(f'{result}\n{type(result)}')
        func_results[col_head] = self_results

    pd.DataFrame(func_results).to_excel(OUTPUT_FILE, sheet_name='Unary_functions', index=False, freeze_panes=(1, 1))

# binary functions (requiring two arguments)
def binary_func_test(selves=def_objects, others=def_objects, functions=def_funcs, OUTPUT_FILE='Binary_functions.xlsx'):
    all_results = {}  # dictionary object with methods as keys and respective dataframes as values.

    for function in functions:

        eval_str = f'{functions[function]}(copy_self_, copy_other)'

        func_results = {'Other': [f'{others[other]}\n{type(others[other])}' for other in others]}

        for self_ in selves:
            col_head = f'{selves[self_]}\n{type(selves[self_])})'
            self_results = []  # list of results in the column 'self'
            for other in others:
                copy_self_ = try_deep_copy(selves[self_])
                copy_other = try_deep_copy(others[other])
                result = try_eval(eval_str, copy_self_, copy_other)  # calculating the result by executing eval on a standard expression
                result = custom_round(result)
                self_results.append(f'{result}\n{type(result)}')
            func_results[col_head] = self_results

        all_results[function] = pd.DataFrame(func_results)

    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='w') as writer:  # a writer object to write multiple sheets
        workbook = writer.book
    
        for function in all_results:
            try:
                workbook.remove(workbook[function])
            except:
                pass
            all_results[function].to_excel(writer, sheet_name=function, index=False, freeze_panes=(1, 1))
    
        writer.save()


if __name__ == '__main__':
    binary_meth_test(selves=more_objs, others=more_objs, methods=def_bin_magics, OUTPUT_FILE='Binary_magic_meths_more_objs.xlsx')