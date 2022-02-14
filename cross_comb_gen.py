# Name: Edwin Joy
# email: edwin7026@gmail.com

from itertools import product

def gen_cross_cov(op_pair, N, hazard, dontcare = False):
    '''
        Generate cross combination coverpoint string

        Input arguments:
            op_pair     :   (tuple) A tuple of instructions between which coverpoint is to be generated
            N           :   (integer) Number of instructions between the op_pair
            hazard      :   (integer) This signifies the type of hazard:
                            0 : RAW
                            1 : WAW
                            2 : RAW
            dontcare    :   (boolean) True: If all the N conditions are not cared for i.e., corresponding
                            conditions are replaced by '?'
                            False: If all combinations of various possible conditions of a hazard is to be returned
        Returns:
            dictionary  :   A dictionary with key as the name of the hazard; values as all combinations of coverpoints
                            of the same hazard. This happens when dontcare is set to True
            string      :   A string is returned when dontcare is set to False 
    '''
    cov_lst = {0: [], 1 : [], 2 : []}
    
    # Op-code list generation
    # Start instruction
    if isinstance(op_pair[0], str):
        opcode_lst = '[ ' + op_pair[0] + ' :' + ''.join(' ? :'* N)
    else:
        opcode_lst = '[('
        for op in op_pair[0]:
            opcode_lst = opcode_lst + op + ','    
        opcode_lst = opcode_lst[:-1] + '):' + ''.join('?:'* N)
    
    # End instruction
    if isinstance(op_pair[1], str):
        opcode_lst += ' ' + op_pair[1] + ' ]'
    else:
        opcode_lst += '('
        for op in op_pair[1]:
            opcode_lst = opcode_lst + op + ','    
        opcode_lst = opcode_lst[:-1] + ')]'

    # Assignment list generation
    assgn_aw = ' a=rd : '
    assgn_ar = ' a=rs1; b=rs2 : '
    assgn_lst_write = ' :: [' + assgn_aw + ''.join(' : ').join('?' * (N+1)) + ' ]'           # For RAW and WAR hazards
    assgn_lst_read = ' :: [' + assgn_ar + ''.join(' : ').join('?' * (N+1))  + ' ]'           # For RAR and RAW hazards

    # Condition list generation
    # Purely non-consuming scenarios
    ncons_w = 'rd!=a and rs1!=a and rs2!=a : '                                              # For read/write after write
    ncons_r = 'rd!=a and rs1!=a and rs2!=a or rd!=b and rs1!=b and rs2!=b : '               # For read/write after read

    #Purely consuming scenarios
    cons_w = 'rs1==a or rs2==a or rd==a : '                                                 # For read/write after write
    cons_r = 'rd==a or rd==b : '                                                            # For read/write after read

    if dontcare:                                                                           # Handling dontcare condition
        if hazard == 0:
            cov = opcode_lst + assgn_lst_write + ' :: [ ? : ' + ''.join(' : ').join('?' * (N)) + ' rs1==a or rs2==a ]'
        elif hazard == 1:
            cov = opcode_lst + assgn_lst_write + ' :: [ ? : ' + ''.join(' : ').join('?' * (N)) + ' rd==a ]'
        elif hazard == 2:
            cov = opcode_lst + assgn_lst_read + ' :: [ ? : ' + ''.join(' : ').join('?' * (N)) + ' rd==a or rd==b ]'
        else:
            raise ValueError('Hazard must be an integer of value 0 to 2')
        return cov
    else:                                                                                   # Generate cross product mapping from 2 to N dimensions
        if hazard == 0 or hazard == 1:
            cond_combination = list(product([cons_w, ncons_w], repeat=N))
        elif hazard == 2:
            cond_combination = list(product([cons_r, ncons_r], repeat=N))
        else:
            raise ValueError('Hazard must be an integer of value 0 to 2')

    for perm in cond_combination:                                                           # Generate coverpoint strings and appending to dictinary
        if hazard == 0:                                 #RAW
            cov_lst[0].insert(0, opcode_lst + assgn_lst_write + ' :: [ ? : ' + ''.join(perm) + 'rs1==a or rs2==a ]')
        elif hazard == 1:                               #WAW
            cov_lst[1].insert(0,  opcode_lst + assgn_lst_write + ' :: [ ? : ' + ''.join(perm) + 'rd==a ]')
        elif hazard == 2:                               #WAR
            cov_lst[2].insert(0, opcode_lst + assgn_lst_read + ' :: [ ? : ' + ''.join(perm) + 'rd==a or rd==b ]')     
    return cov_lst

if __name__ == '__main__':
    #Op-code list input
    start_ops = ('add')
    end_ops = ('mul')
    op_pair_ = (start_ops, end_ops)
    N = 2
    dc = True
    haz_dict = {0 : 'RAW', 1 : 'WAW', 2 : 'WAR'}
    if dc:
        for i in range(3):
            print('{} hazards with dont cares'.format(haz_dict[i]))
            print(gen_cross_cov(op_pair_, N, i, dc))
    else:
        for i in range(3):
            print('{} hazards for Consuming and Non-consuming scenarios'.format(haz_dict[i]))
            for cov in gen_cross_cov(op_pair_, N, i, dc)[i]:
                print(cov)
