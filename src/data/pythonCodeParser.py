# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:24:48 2021

@author: Anil


Python code parser

"""
#python code parser
import ast




def getAllNodeTypes(expr):    
    try:
      parser = PythonCodeParser(expr)
      return parser.nodeTypes
    except:
      return ''

def getAllNodeTypesUsefull(expr):    
    try:
      parser = PythonCodeParser(expr)
      return parser.nodeTypesUsefull
    except:
      return ''


def resolve_negative_literals(_ast):

    class RewriteUnaryOp(ast.NodeTransformer):
        def visit_UnaryOp(self, node):
            if isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Num):
                node.operand.n = 0 - node.operand.n
                return node.operand
            else:
                return node

    return RewriteUnaryOp().visit(_ast)

ProgramConceptsExpressions = [
#        'Expr'
#        
#        , 
 
            'UnaryOp', 'UAdd', 'USub' ,
         'Not', 'Invert', 'BinOp' ,
         'Add' , 'Sub', 'Mult' , 'Div', 'FloorDiv'  ,
         'Mod' , 'Pow'  ,
         'LShift' , 'RShift' ,
         'BitOr' , 'BitXor' , 'BitAnd' ,
         'MatMult' , 'BoolOp' ,
        
         'And' , 'Or' , 'Compare'  , 'Eq' ,
         'NotEq' , 'Lt'  , 'LtE' , 'Gt' , 'GtE' ,
         'Is' , 'IsNot'  ,
         'In' , 'NotIn' ,
        
         'Call' , 'keyword' , 'IfExp',        
        ]


ProgramConceptsSubscripting = [
        'Subscript' ,
        'Slice' ,
        ]

ProgramConceptsComprehensions = [
        'ListComp' ,
        'SetComp' , 'GeneratorExp', 'DictComp', 'comprehension'      ,   
        ]

ProgramConceptsStatements = [
        'Assign' ,
        'AnnAssign' , 'AugAssign', 'Raise', 'Assert', 'Delete', 'Pass' ,
        ]

ProgramConceptsImports = [
        'Import' ,
        'ImportFrom' , 'alias' ,
        ]
ProgramConceptsControlFlow = [
        'If' ,
        'For' , 'While', 'Break', 'Continue', 'Try', 'ExceptHandler'  ,      
        'With' , 'withitem' ,
        ]
ProgramConceptsFunctionClass  = [
        'FunctionDef'  ,
        'Lambda' , 'arguments', 'arg', 'Return', 'Yield', 'YieldFrom'   ,      
        'Global' , 'Nonlocal',
        
        'ClassDef'
        ]

ProgramConceptsAsync   = [
        'AsyncFunctionDef'    ,     
        'Await' , 'AsyncFor', 'AsyncWith'
        ]

ProgramConceptsVariables   = [
#        'Name' ,
#        , 'Load' 
        'Store', 'Del' , 'Starred' ,
        ]
    
ProgramConstants   = [
        'Constant'
        , 'FormattedValue' , 'JoinedStr', 'Str' , 'List' , 'Tuple' , 'Set' , 'Dict'
        ]



ProgramConceptsUsefull = [

                   'BitAnd', 'BitOr', 'BitXor', 'BoolOp', 'LShift', 'BoolOp', 'UAdd', 'USub', 'UnaryOp',
                   'Add', 'Div', 'Gt',  'GtE', 'Is',  'IsNot','Lt',  'LtE', 'MatMult',  'Mult',   'NotEq',  'NotIn', 'Sub', 
                   'And', 'Or', 'Not',
                   'Assert', 'Break', 'Compare', 'Constant', 'Del', 'Delete', 'If', 'IfExp',  'In',  'While',  
                   'ClassDef', 'Dict', 'FunctionDef', 'Global', 'List', 'ListComp', 'Mod', 
#                   'Module',  
                   'Param',  'Return', 'Set', 
                   'Continue', 'For', 
                   'ExceptHandler',  'Import', 'Invert', 'JoinedStr', 'NameConstant',  'Try',
                   'Num', 'Str', 'Expression', 'Import', 'Invert', 'JoinedStr',
                   
                   'Assign' , 'AugAssign' , 'AnnAssign'    ,
                   ]


ProgramConceptsUsefull = ( ProgramConceptsUsefull + ProgramConceptsExpressions + ProgramConceptsAsync
                          + ProgramConceptsFunctionClass + ProgramConceptsControlFlow + ProgramConceptsImports + ProgramConceptsStatements
                          + ProgramConceptsComprehensions + ProgramConceptsSubscripting 
                          + ProgramConceptsVariables + ProgramConstants)

ProgramConceptsUsefull = set(ProgramConceptsUsefull)
ProgramConceptsUsefull = list(ProgramConceptsUsefull)



#-----------------------------------------------------------------------------------------
# PYTHON CODE PARSER
#----------------------------------------------------------------------------------------
class PythonCodeParser:
    def __init__(self, expr):
        self.expr = expr
        self.tree = ast.parse(self.expr, mode="exec")
        self.tree = resolve_negative_literals(self.tree)
        
#        count lines of code
        self.countLineOfCode = 0
        
#        node types  - create an empty set and fill it
        self.nodeTypes = {''}
        self.nodeTypes = self.getAllNodeTypes()
        self.nodeTypesUsefull = list(self.nodeTypes.intersection(ProgramConceptsUsefull))
        
    
# 1 :   Common programming concepts
    def hasLoop(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    return True
        return False
    
    def hasNestedLoop(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    for nodeChild in ast.iter_child_nodes(node):
                        if isinstance(nodeChild, (ast.For, ast.While)):
                            return True
        return False

    def hasCondition(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.If)):
                    return True
        return False

    def hasVariable(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Store, ast.NameConstant,   ast.Starred  )):
                    return True
        return False
    
    
    def hasRecursion(self):
        
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    for nodeChild in ast.iter_child_nodes(node):
                        if isinstance(nodeChild, (ast.For, ast.While)):
                            return True
        return False
    
    
    def resolve_negative_literals(_ast):
    
        class RewriteUnaryOp(ast.NodeTransformer):
            def visit_UnaryOp(self, node):
                if isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Num):
                    node.operand.n = 0 - node.operand.n
                    return node.operand
                else:
                    return node
    
        return RewriteUnaryOp().visit(_ast)
    
    
# 2 :   Lines of Code
    
    def countLinesOfCode(self):
        self.countLineOfCode  = self.expr.count('\n')
        return self.countLineOfCode

    def visit(self):
        self.node_count += 1
        try:
            
            self.line_numbers2 = self.tree.lineno
            self.line_numbers.add(self.tree.lineno)
        except AttributeError:
            pass
        self.visit(self.tree)

    @property
    def density(self):
        """The density of code (nodes per line) in the visited AST."""
        return self.node_count / len(self.line_numbers)
    
    
# 3 :   All Node types - all concepts used
    
    def getAllNodeTypes(self):    
        for node in [n for n in ast.walk(self.tree)]:
            self.nodeTypes.add( node.__class__.__name__ )
            
        return self.nodeTypes


# 4.1 Subset programming concepts Classes
    def hasExpressionsArithematic(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Add,  ast.Sub,  ast.Mult,  ast.Div,  ast.FloorDiv,  ast.Mod,  ast.Pow )):
                    return True
        return False

    def hasExpressionsBool(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.And,  ast.Or )):
                    return True
        return False

    def hasExpressionsLogical(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Compare,  ast.Eq,  ast.NotEq,  ast.Lt
                                     ,  ast.LtE,  ast.Gt,  ast.GtE,  ast.Is,  ast.IsNot,  ast.In,  ast.NotIn )):
                    return True
        return False
   
    def hasExpressionsUnary(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.UnaryOp, ast.Not,  ast.Invert
                                     ,  ast.UAdd ,  ast.USub  )):
                    return True
        return False
    
    def hasExpressionsBitwise(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.LShift,  ast.RShift,  ast.BitOr,  ast.BitXor,  ast.BitAnd,  ast.MatMult
                                     ,  ast.BoolOp )):
                    return True
        return False

    def hasExpressionsDict(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Dict )):
                    return True
        return False

    def hasExpressionsDataStructure(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Dict, ast.List, ast.Set )):
                    return True
        return False

    def hasExpressionsKeyword(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.keyword )):
                    return True
        return False

    def hasExpressionsFunctionCall(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Call )):
                    return True
        return False
    
    def hasControlFlowConditional(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.If,  ast.Break,  ast.Continue
                                     , ast.With,  ast.withitem )):
                    return True
        return False

    def hasControlFlowTryException(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Try,  ast.ExceptHandler )):
                    return True
        return False

    def hasVariablesNamed(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Name,   ast.NameConstant,  ast.Starred ,  )):
                    return True
        return False

    def hasConstantsUseful(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.Str,
                                     ast.NameConstant, ast.Num )):
                    return True
        return False


# 4 :   Generic programming concepts Classes
    def hasExpressions(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.Expr,  ast.UnaryOp,  ast.UAdd,  ast.USub,  ast.Not,  ast.Invert
                                     ,  ast.BinOp,  ast.Add,  ast.Sub,  ast.Mult,  ast.Div,  ast.FloorDiv,  ast.Mod,  ast.Pow
                                     ,  ast.LShift,  ast.RShift,  ast.BitOr,  ast.BitXor,  ast.BitAnd,  ast.MatMult
                                     ,  ast.BoolOp,  ast.And,  ast.Or,  ast.Compare,  ast.Eq,  ast.NotEq,  ast.Lt
                                     ,  ast.LtE,  ast.Gt,  ast.GtE,  ast.Is,  ast.IsNot,  ast.In,  ast.NotIn,  ast.Call
                                     ,  ast.keyword,  ast.IfExp,  ast.Attribute)):
                    return True
        return False

    def hasAsyncOrAwait(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.AsyncFunctionDef,  ast.Await,  ast.AsyncFor,  ast.AsyncWith)):
                    return True
        return False
    

    def hasFunctionClass(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.FunctionDef,  ast.Lambda,  ast.arguments,  ast.arg,  ast.Return,  ast.Yield,  ast.YieldFrom,  ast.Global,  ast.Nonlocal,  ast.ClassDef)):
                    return True
        return False

    def hasControlFlow(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.If,  ast.For,  ast.While,  ast.Break,  ast.Continue
                                     ,  ast.Try,  ast.ExceptHandler,  ast.With,  ast.withitem )):
                    return True
        return False
    
    
    def hasImports(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Import,  ast.ImportFrom,  ast.alias )):
                    return True
        return False

    def hasStatements(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Assign,  ast.AnnAssign,  ast.AugAssign,  ast.Raise
                                     ,  ast.Assert,  ast.Delete,  ast.Pass )):
                    return True
        return False
    
    def hasComprehensions(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.ListComp,  ast.SetComp,  ast.GeneratorExp,  ast.DictComp,  ast.comprehension )):
                    return True
        return False
    
    def hasSubscripting(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.Subscript,  ast.Slice )):
                    return True
        return False

    
    def hasConstants(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.Str, ast.NameConstant, ast.Num
                                     , ast.List  ,   ast.Tuple ,  ast.Set, ast.Dict  )):
                    return True
        return False

    def hasVariables(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Name, ast.Load, ast.Store
                                     , ast.Del  ,   ast.Starred  )):
                    return True
        return False