# **LFX-riscv-isac-task**
## **TASK 1:** Coverpoint generator for a cross combination coverpoint in riscv-isac

Executing the python file cross_comb_gen.py out of the box would produce a combination of all possible coverpoints for add and mul instructions with N instructions between them. The combinations of coverpoints include both consuming and non-consuming scenarios.

*Features*
- gen_cross_cov() method in cross_comb_gen.py generates all possible coverpoints for a given set of op-codes and hazards for both consuming and non-consuming scenarios. The following are its arguments.
    - Start and end op-codes tuple.
    - Number of instructions between  start and end op-codes.
    - Type of hazard: RAW, WAW, WAR. (RAR is not considered to be a data hazard).
    - If the conditons for N op-codes are to be cared. If true, the method would return a string with dontcare conditons i.e. '?'.
- Code reusability was kept in mind. gen_cross_cov() returns a dictionary of all possible hazards which makes it easy to integrate into the .cgf file.
- gen_cross_cov() can handle both op-code string and tuples as shown in the examples for cross-comb coverpoint format.
- Since code in cross() class in riscv-isac is white-space dependent, white spaces are handled properly to ensure compatibility.

*Manual Solution*
- Considering the coverpoint: [ add : ? : ? : mul ] :: [a=rd : ? : ? : ?] :: [? : rd!=a and rs1!=a and rs2!=a : rs1==a or rs2==a or rd==a : rd==a]
    - This coverpoint is used to check for WAW data hazard 
- Possible Solutions:
    - A classic and easy way to get rid of data hazards is by appending nop instruction between hazardous instructions in the pipeline. But this is not desired as it contradicts the very need for pipelining.
    - Hardware level optimization of pipelining should be implemented. e.g. data forwarding.
    - riscv-isac can find and initiate a instruction reordering scheme to be safe from data hazards. This can involve pushing independent instructions from the code into the pipeline between hazardous instructions

## **TASK 2:** Generate test report using riscof framework for RISCV-64I 
The test report in accordance with task 2 is given
*Issues*
- There are 24 failed tests in the report. This may be due to editing the spike and cSail yaml files for making it compatible for RISC-V64I
