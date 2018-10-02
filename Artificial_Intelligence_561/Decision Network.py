import copy

Parents_vlist_dic = {}   #store the parents of a given nodelist
Memory_vlist_dic = {}    #store the calculated subprobability for reuse

class Node:
    def __init__(self, name, parents, cpt):
        self.name = name
        self.parents = parents
        self.cpt = cpt


def GenerateListParents(nodelist):
    vlist = ""
    pre_parents_vlist = []
    for i in range(len(nodelist) - 1, -1, -1):
        vlist = nodelist[i].name + vlist
        if nodelist[i].name in pre_parents_vlist:
            pre_parents_vlist.remove(nodelist[i].name)
        if nodelist[i].parents[0] != "decision" and nodelist[i].parents[0] != "start":
            for p in nodelist[i].parents:
                if not p in pre_parents_vlist:
                    pre_parents_vlist.append(p)
        pre_parents_vlist.sort()
        Parents_vlist_dic[vlist] = copy.deepcopy(pre_parents_vlist)

#More to improve: Only need to calculate the probability in the inference chain. Probability of other nodes will be marginalized to 1.
def MarginalProbability(vlist, evdic):     #calculate the marginal probability by enumeration with memory
    if len(vlist) == 0:
        return 1

    memory_name = ""        #generate memory name according to parents' values and evidence nodes' values
    for v in vlist:
        memory_name += v.name
    parents_vlist = Parents_vlist_dic[memory_name]
    memory_name = ":" + memory_name
    for i in range(len(vlist)-1, -1, -1):
        if evdic.has_key(vlist[i].name):
            memory_name = vlist[i].name + "=" + str(evdic[vlist[i].name]) + memory_name
    for i in range(len(parents_vlist)-1, -1, -1):
        memory_name = parents_vlist[i] + "=" + str(evdic[parents_vlist[i]]) + memory_name

    if Memory_vlist_dic.has_key(memory_name):    #reuse memorized value
        return Memory_vlist_dic[memory_name]

    node = vlist.pop(0)
    if node.parents[0] == "decision":
        p = MarginalProbability(vlist, evdic)
        Memory_vlist_dic[memory_name] = p
        return p
    elif node.parents[0] == "start":
        cp = node.cpt[0]
    else:
        deccode = 0
        for i in range(len(node.parents)-1, -1, -1):
            if evdic[node.parents[i]] == 1:
                deccode += pow(2, len(node.parents)-i-1)
        cp = node.cpt[deccode]

    if evdic.has_key(node.name):
        if evdic[node.name] == 1:
            p = cp * MarginalProbability(vlist, evdic)
        else:
            p = (1 - cp) * MarginalProbability(vlist, evdic)
    else:
        evdic[node.name] = 1
        subp1 = cp * MarginalProbability(copy.deepcopy(vlist), copy.deepcopy(evdic))
        evdic[node.name] = 0
        subp2 = (1 - cp) * MarginalProbability(vlist, evdic)
        p = subp1 + subp2
    Memory_vlist_dic[memory_name] = p   #memorize calculated value
    return p


def QueryProbability(nodelist, variables, values, evdic):
    allvalues = []
    for i in range(0, pow(2, len(variables))):  #enumerate all possible sets of values of variables
        i = bin(i)[2:].zfill(len(variables))
        allvalues.append(i)

    for i in range(0, len(variables)):
        evdic[variables[i]] = values[i]
    p = MarginalProbability(copy.deepcopy(nodelist), copy.deepcopy(evdic))

    sump = 0
    for av in allvalues:
        for i in range(0, len(variables)):
            evdic[variables[i]] = int(av[i])
        sump += MarginalProbability(copy.deepcopy(nodelist), copy.deepcopy(evdic))

    return p/sump  #normalization


def EU(nodelist, utilitynode, evdic):
    variables = []
    allvalues = []
    for i in range(0, len(utilitynode.parents)):
        if not evdic.has_key(utilitynode.parents[i]):
            variables.append(utilitynode.parents[i])
    for i in range(0, pow(2, len(variables))):        #enumerate all possible sets of values of utility node's parents
        i = bin(i)[2:].zfill(len(variables))
        allvalues.append(i)

    sump = 0
    eu = 0
    for av in allvalues:
        evdic2 = copy.deepcopy(evdic)
        for i in range(0, len(utilitynode.parents)):
            if not evdic2.has_key(utilitynode.parents[i]):
                evdic2[utilitynode.parents[i]] = int(av[0])
                av = av[1:]

        p = MarginalProbability(copy.deepcopy(nodelist), copy.deepcopy(evdic2))
        sump += p

        deccode = 0
        for i in range(len(utilitynode.parents) - 1, -1, -1):
            if evdic2[utilitynode.parents[i]] == 1:
                deccode += pow(2, len(utilitynode.parents) - i - 1)

        eu += p * utilitynode.cpt[deccode]

    return eu/sump


def MEU(nodelist, utilitynode, evdic, decisions):
    alldecisions = []
    for i in range(0, pow(2, len(decisions))):  ##enumerate all possible sets of values of decisions
        i = bin(i)[2:].zfill(len(decisions))
        alldecisions.append(i)

    max_eu = 0
    opt_decision = 0
    for ad in alldecisions:
        for i in range(0, len(decisions)):
            evdic[decisions[i]] = int(ad[i])
        eu = EU(nodelist, utilitynode, evdic)
        if eu > max_eu:
            max_eu = eu
            opt_decision = ad

    opt_decision_output = ""
    for i in range(0,len(opt_decision)):
        if opt_decision[i] == "1":
            opt_decision_output += "+ "
        else:
            opt_decision_output += "- "
    opt_decision_output += "%d" % round(max_eu, 0)

    return opt_decision_output


if __name__ == "__main__":

    readlines = []
    input_file = open("input.txt", 'r')
    while True:
        readline = input_file.readline()
        if readline != "":
            readlines.append(readline.strip())
        if not readline:
            break
    input_file.close()

    queries = []
    nodelist = []

    i = 0
    while i < len(readlines) and readlines[i] != "******":
        queries.append(readlines[i])                         #fetch queries
        i += 1
    i += 1

    while i < len(readlines):
        linelist = readlines[i].split(" ")       #fetch nodes
        name = linelist[0]
        if len(linelist) == 1:
            if readlines[i+1].split(" ")[0] == "decision":       #decision node
                decisionnode = Node(name, ["decision"], [])
                nodelist.append(decisionnode)
            else:
                startnode = Node(name, ["start"], [float(readlines[i+1].split(" ")[0])])   #node with no parent
                nodelist.append(startnode)
            i += 3
            continue

        parents = []
        for j in range(2, len(linelist)):
            parents.append(linelist[j])
        cpt = []
        for j in range(0, pow(2, len(parents))):       #generate cpt
            cpt.append(0)
        j = 1
        while i + j < len(readlines) and readlines[i+j][0] != "*":   #encode the value into binary number and then into decimal number
            deccode = 0
            linelist = readlines[i+j].split(" ")
            p = linelist[0]
            for k in range(len(linelist)-1, 0, -1):
                if linelist[k] == "+":
                    deccode += pow(2, len(linelist)-k-1)
            cpt[deccode] = float(p)
            j += 1

        if name != "utility":
            nodelist.append(Node(name, parents, cpt))   #add nodes into BN except the utility node
        else:
            utilitynode = Node(name, parents, cpt)
        i += j + 1

    GenerateListParents(nodelist)

    output_text = ""

    for query in queries:
        if query[0] == "P":    #parse probability queries
            variables = []
            values = []
            evdic = {}
            query = query[2:len(query)-1]
            variables_sen = query.split(" | ")[0]
            variables_list = variables_sen.split(", ")
            for v in variables_list:
                variables.append(v.split(" = ")[0])
                value = v.split(" = ")[1]
                if value == "+":
                    values.append(1)
                else:
                    values.append(0)
            if len(query.split(" | ")) > 1:
                evidences_sen = query.split(" | ")[1]
                evidences_list = evidences_sen.split(", ")
                for ev in evidences_list:
                    name = ev.split(" = ")[0]
                    value = ev.split(" = ")[1]
                    if value == "+":
                        evdic[name] = 1
                    else:
                        evdic[name] = 0
            p = QueryProbability(nodelist, variables, values, evdic)
            output_text += "%.2f" % p + "\n"

        elif query[0] == "E":    #parse EU queries
            evdic = {}
            query = query[3:len(query) - 1].replace(" | ", ", ")
            evidences_list = query.split(", ")
            for ev in evidences_list:
                name = ev.split(" = ")[0]
                value = ev.split(" = ")[1]
                if value == "+":
                    evdic[name] = 1
                else:
                    evdic[name] = 0
            eu = EU(nodelist, utilitynode, evdic)
            output_text += "%d" % round(eu,0) + "\n"

        else:                 #parse MEU queries
            decisions = []
            evdic = {}
            query = query[4:len(query) - 1]
            decisions_sen = query.split(" | ")[0]
            decisions = decisions_sen.split(", ")

            if len(query.split(" | ")) > 1:
                evidences_sen = query.split(" | ")[1]
                evidences_list = evidences_sen.split(", ")
                for ev in evidences_list:
                    name = ev.split(" = ")[0]
                    value = ev.split(" = ")[1]
                    if value == "+":
                        evdic[name] = 1
                    else:
                        evdic[name] = 0
            output_text += MEU(nodelist, utilitynode, evdic, decisions) + "\n"

    output_file = open('output.txt', 'w')
    output_file.write(output_text)
    output_file.close()