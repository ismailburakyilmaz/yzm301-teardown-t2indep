"""Thin MCP stdio adapter; all semantic validation/calculation is shared."""
import asyncio
import json
from mcp import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent, CallToolResult, ListToolsResult
from .interface import execute,error
from . import __version__

NUMERICAL_MESSAGE = 'calculation failed: non-finite or unresolved numerical result'


def input_variant(mode):
    props = dict(test={'type':'string','const':'t2-indep'},mode={'type':'string','const':mode},
                 tails={'type':'integer','enum':[1,2]},d={'type':'number','exclusiveMinimum':0,'maximum':20},
                 alpha={'type':'number','minimum':1e-7,'exclusiveMaximum':1})
    if mode == 'a-priori':
        props.update(power={'type':'number','minimum':1e-7,'exclusiveMaximum':1},
                     ratio={'type':'number','minimum':0.01,'maximum':100})
    else:
        props.update(n1={'type':'integer','minimum':2},n2={'type':'integer','minimum':2})
    return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}


# Semantic errors, including foreign public-vector fields, belong to the same
# adapter as CLI. Avoid SDK enum/type/required guards replacing its error JSON.
INPUT_SCHEMA = {'type':'object','properties':{f:{} for f in ('test','mode','tails','d','alpha','power','ratio','n1','n2')},'additionalProperties':True}


def result_variant(fields):
    return {'type':'object','properties':{f:{'type':'integer' if f in ('n1','n2','n_total','df') else 'number'} for f in fields},
            'required':list(fields),'additionalProperties':False}


OUTPUT_SCHEMA = {'type':'object','oneOf':[
    result_variant(('n1','n2','n_total','actual_power','critical_t','df','ncp')),
    result_variant(('power','critical_t','df','ncp')),
    {'type':'object','properties':{'error':{'type':'string','minLength':1},'code':{'type':'string'},'field':{'type':['string','null']}},'required':['error','code','field'],'additionalProperties':False}]}
TOOL = Tool(name='power_analysis',description='İki bağımsız grubun t testi: a priori veya post hoc. '
            'N2/N1 tahsisi; başka test ailesi desteklenmez. Bilinen uç sayısal uyumsuzluklar raporlanmıştır.',
            input_schema=INPUT_SCHEMA,output_schema=OUTPUT_SCHEMA)


def invoke(arguments):
    code,result=execute(arguments)
    return code!=0,result


async def list_tools(ctx,params):
    return ListToolsResult(tools=[TOOL])


async def call_tool(ctx,params):
    if params.name != TOOL.name:
        failed,result = True,error('UNSUPPORTED',None,'Desteklenmeyen araç adı')
    else:
        failed,result = invoke(params.arguments if params.arguments is not None else {})
    return CallToolResult(content=[TextContent(type='text',text=json.dumps(result,ensure_ascii=True,allow_nan=False,separators=(',',':')))],
                          structured_content=result,is_error=failed)


server = Server('independent-t-power',version=__version__,on_list_tools=list_tools,on_call_tool=call_tool)


async def serve():
    async with stdio_server() as (reader,writer):
        await server.run(reader,writer,server.create_initialization_options())


def main():
    asyncio.run(serve())


if __name__ == '__main__':
    main()
