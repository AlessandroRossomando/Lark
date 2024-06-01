# - the loop variable can be only one of i, j
# - the loop has the syntax


#   for(var=const;var op const; varOP) {
#     instr;
# }

# where const are integer constants, op is a comparison operator among
# the two < and >, varOP is var++ or var—
# - instr can have only the structure
#
#  z += var op const;

# where op is + or * (sum or product); += is equivalent to z = z + …
# - at the end of the loop print the value of z


from lark import Lark, Transformer

# import token

grammar = r"""
    for_loop: "for" "(" assignment ";" condition ";" iteration ")" "{" instruction "}"
    
    assignment: INDEX_I "=" INT  
               | INDEX_J "=" INT  
    
    condition: INDEX_I MINOR_OP INT | INDEX_I GREATER_OP INT 
             | INDEX_J MINOR_OP INT | INDEX_J GREATER_OP INT
             
    iteration: INDEX_I INC | INDEX_I DEC 
             | INDEX_J INC | INDEX_J DEC
    
    instruction: "z" "+=" INDEX_I PLUS INT ";" | "z" "+=" INDEX_I MULT INT ";" 
               | "z" "+=" INDEX_J PLUS INT ";" | "z" "+=" INDEX_J MULT INT ";"

    INT: /[0-9]+/
    INDEX_I: "i" 
    INDEX_J: "j"
    GREATER_OP:  ">"
    MINOR_OP: "<" 
    INC: "++" 
    DEC: "--"
    PLUS: "+" 
    MULT : "*"

    %ignore /\s+/
"""


class MyTransformer(Transformer):

    def for_loop(self, args):

        assignment, condition, iteration, instruction = args
        # costruito il parse tree posso inizializzare le variabili per il ciclo
        index_loop, start_value = assignment
        index_cond, cond_op, end_value = condition
        index_iter, inc_dec = iteration
        index_instr, operator, const = instruction
        z = 0
        # controllo che la sintassi del codice sia corretta {i;i;i}
        if index_loop != index_cond or index_loop != index_iter or index_loop != index_instr:
            print('Error: Loop index mismatch.')
        # CICLO FOR
        while self.loop_condition(start_value, cond_op, end_value):
            z = self.execute_instruction(z, start_value, operator, const)
            start_value = self.update_variable(start_value, inc_dec)
            print(60 * "_")

        print("Final result:", z)
        return assignment, condition, iteration, instruction

    def assignment(self, args):

        index_loop, start_value = args
        return index_loop, int(start_value)

    def condition(self, args):

        index_cond, comp_op, end_value = args
        return index_cond, comp_op, int(end_value)

    def iteration(self, args):

        index_iter, inc_dec = args
        return index_iter, inc_dec

    def instruction(self, args):

        index_instr, operator, const = args
        return index_instr, operator, int(const)

    def index_i(self, args):
        return args

    def index_j(self, args):
        return args

    def greater_op(self, args):
        return args

    def minor_op(self, args):
        minor, greater = args
        return minor, greater

    def dec(self, args):
        return args

    def inc(self, args):
        return args

    def plus(self, args):
        return args

    def mult(self, args):
        return args

    # CODICE PER IL CICLO

    def loop_condition(self, index_cond, op_comp, end_value):
        print("loop_condition")
        if op_comp == "<":
            print(f"{index_cond} {op_comp} {end_value}"" stampa delle condizione loop")
            return index_cond < end_value
        elif op_comp == ">":
            print(f"{index_cond} {op_comp} {end_value}"" stampa delle condizione loop")
            return index_cond > end_value

    def update_variable(self, index_iter, op_up):
        print("update_variable")
        if op_up == "++":
            index_iter += 1
            print(f"{index_iter}" " stampa dell' incremento")
        elif op_up == "--":
            index_iter -= 1
            print(f"{index_iter}" " stampa dell' incremento")
        return index_iter

    def execute_instruction(self, z, index_instr, op_instr, const):
        print("execute_instruction")

        if op_instr == "+":
            result = index_instr + const
            print(f"{result}" " stampa intermedia prima di sommarla a z ")
            z += result
            print(f"{z}" " stampa di z")
            # z += f"{index_instr} {op_instr} {int(const)} "
        if op_instr == "*":
            result = index_instr * const
            print(f"{result}"" stampa intermedia prima di sommarla a z ")
            z += result
            print(f"{z}"" stampa di z")
        #   z += f"{index_instr} {op_instr} {const} "
        return z


code = """
for(j=0;j<7;j++) {
    z += j + 2;
}
"""
parser = Lark(grammar, start='for_loop', parser='lalr', transformer=MyTransformer())
result = parser.parse(code)
# print(result)
# eval_tree = MyTransformer().transform(result)