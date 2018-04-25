import itertools
from string import ascii_letters


def convert_to_rpn(inputstr):
    stack = []
    output = []
    operators = {'&': 4, '|': 2, '!': 3, '>': 5, '=': 6, '~': 7, '(': 1}  # without '~':6 !!!
    for character in inputstr:
        if character == '(':
            stack.append(character)
        elif character == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif character not in operators:
            output.append(character)
        else:
            while stack != [] and operators[character] <= operators[stack[-1]]:
                temp = stack.pop()
                output.append(temp)
            stack.append(character)
    while stack != []:
        output.append(stack.pop())
    return output


def my_not(val):
    if val == 0:
        return 1
    return 0


def my_and(a, b):
    if a == 1 and b == 1:
        return 1
    return 0


def my_or(a, b):
    if a == 1 or b == 1:
        return 1
    return 0


def my_xor(a, b):
    if my_or(a, b) == 1 and my_not(my_and(a, b)) == 1:
        return 1
    return 0


def my_imp(a, b):
    if a == 1 and b == 0:
        return 0
    return 1


def my_equ(a, b):
    return my_not(my_xor(a, b))


def evaluate_rpn(input):
    stack = []
    operators = {'&': 4, '|': 2, '!': 3, '>': 5, '=': 6, '~': 7, '(': 1}
    for element in input:
        if element == 0 or element == 1:
            stack.append(element)
        elif element == '~':
            stack.append(my_not(stack.pop()))
        else:
            b = stack.pop()
            a = stack.pop()
            if element == '&':
                stack.append(my_and(a, b))
            elif element == '|':
                stack.append(my_or(a, b))
            elif element == '!':
                stack.append(my_xor(a, b))
            elif element == '>':
                stack.append(my_imp(a, b))
            elif element == '=':
                stack.append(my_equ(a, b))
    return stack.pop()


def var_with_rep(n):
    return list([list(x) for x in itertools.product([1, 0], repeat=n)])


def combinations(pattern):
    variables = sorted(set([x for x in pattern if x in ascii_letters]))
    values = var_with_rep(len(variables))
    ret1 = []

    for valset in values:
        ret = []
        for element in pattern:
            if element in ascii_letters:
                ret.append(valset[variables.index(element)])
            elif element == '1':
                ret.append(1)
            elif element == '0':
                ret.append(0)
            else:
                ret.append(element)
        ret1.append((([dict(zip(variables, valset))], dict(zip(variables, valset))), ret))
    return ret1


def is_prime_imp(expr):
    return evaluate_rpn(expr) == 1


def get_1st_prime_implicants(list):
    return [x[0] for x in list if is_prime_imp(x[1])]


def sort_by_ones(implicants):
    onescount = 0
    end = len(implicants)
    state = 0
    outdict = {}
    while state < end:
        outdict[onescount] = [x for x in implicants if sum(x[1].values()) == onescount]
        state += len(outdict[onescount])
        onescount += 1
    return outdict


def finddif(dict1, dict2):
    vardif = []
    for key in dict1.keys():
        if dict1[key] != dict2[key]:
            vardif.append(key)
    return vardif


def possibilities(l1, l2, last):
    poss = []
    if l1==[]:
        poss = poss + l2
        return poss

    for t1 in l1:
        used = False
        for t2 in l2:
            dif = finddif(t1[1], t2[1])
            if len(dif) == 1:
                used = True
                tmp = t1[1].copy()
                tmp[dif[0]] = None
                poss.append((t1[0] + t2[0], tmp))
        if used == False:
            poss.append(t1)
            if last:
                poss.append(t2)
    return poss


def dictpos(byones):
    l, r = 0, 1
    outdict = {}
    while r < len(byones):
        outdict[l] = possibilities(byones[l], byones[r], r == len(byones))
        l += 1
        r += 1
    return outdict


def samevalues(el1, el2):
    for i in el1:
        if i not in el2:
            return False
    return True


def remdup(withdup):
    ret = []
    for el1 in withdup:
        flag = True
        for el2 in ret:
            if samevalues(el1[0], el2[0]):
                flag = False
        if flag:
            ret.append(el1)
    return ret


def allimplicants(byones):
    while len(dictpos(byones).keys()) != 1:  # != {0: []}:
        byones = dictpos(byones)
        for key in byones.keys():
            byones[key] = remdup(byones[key])
    return byones


def with_specific(impls, prime):
    hld = []
    for impl in impls:
        if prime in impl[0]:
            hld.append(impl)
    return hld


def get_essentials(impls, primes):
    hld = []
    for prime in primes:
        a = with_specific(impls, prime)
        if len(a) == 1:
            hld.append(a[0])
    return remdup(hld)


def solutions(values):
    res = []
    for i in range(0, len(values) + 1):
        res = res + list(map(list, itertools.combinations(values, i)))
    return res


def remdup2(withdup):
    ret = []
    for el1 in withdup:
        flag = True
        for el2 in ret:
            if el1 == el2:
                flag = False
        if flag:
            ret.append(el1)
    return ret


def get_coverage(solution):
    solpart = [x for x in solution]
    solutions = [x[0] for x in solpart]
    out = [j for i in solutions for j in i]
    return remdup2(out)


def check_list_eq(l1, l2):
    if len(l1) != len(l2):
        return False
    for e1 in l1:
        if e1 not in l2:
            return False
    return True


def conv_conjunction(conjunction):
    outputstr = ""
    for var in conjunction:
        if conjunction[var] == 1:
            outputstr += var
            outputstr += '&'
        elif conjunction[var] == 0:
            outputstr += "(~" + var + ')'
            outputstr += '&'
    return outputstr[:-1]


def convert_to_string(disjunction):
    outputstr = ""
    if disjunction == None:
        return outputstr
    for conjunction in disjunction:
        outputstr += conv_conjunction(conjunction) + '|'
    return outputstr[:-1]


def simplify(prepexpr):
    rpnexpr = convert_to_rpn(prepexpr)
    rpncombinations = combinations(rpnexpr)
    primes = get_1st_prime_implicants(rpncombinations)

    if(len(primes)==0):
        return ("0")
    if(len(primes)==2**len(primes[0][1])):
        return ("1")

    firstimplbyones = sort_by_ones(primes)

    implicantlist = [j for i in list(allimplicants(firstimplbyones).values()) for j in i]
    primeslist = [x[1] for x in primes]

    essentials = get_essentials(implicantlist, primeslist)

    implicantlist = [x for x in implicantlist if x not in essentials]  # remove essentials

    essentialsprimes = [x[0] for x in essentials]
    essentialsprimes = [j for i in essentialsprimes for j in i]

    primeslist = [x for x in primeslist if x not in essentialsprimes]  # remove essentials

    possiblesolutions = solutions(implicantlist)

    ret = None

    for sol in possiblesolutions:
        if check_list_eq(get_coverage(sol), primeslist):
            ret = sol + essentials

    if ret != None:
            ret = [x[1] for x in ret]
    return convert_to_string(ret)


print(simplify("a!c"))