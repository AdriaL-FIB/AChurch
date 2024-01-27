from achurch import TreeVisitor, parseInput, macros, MacroNoDefinit
from arbre import *
import pydot

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'AChurchBot!\nBenvingut {update.effective_user.first_name} !')

async def author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'AChurchBot!\n@ Adrià Lozano, 2023')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'/start\n/author\n/help\n/macros\nExpressió λ-càlcul')

async def macrosF(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print llista de macros
    msg = ""
    for [macroName, terme] in macros.items():
        msg += macroName + " ≡ " + string(terme) + "\n"

    if msg == "":
        msg = "No hi ha macros definits"
    await update.message.reply_text(msg)

node_count = 0
parent = dict()

def create_graph(g: pydot.Dot, t: Arbre):
    global node_count
    match t:
        case Aplicacio(esq, dre):
            id_node = node_count
            node_count += 1
            g.add_node(pydot.Node(name=str(id_node), label="@", shape="none"))


            id_child = create_graph(g, esq)
            nodeEsq = g.get_node(str(id_child))[0]
            nodeEsq.set("ordering", "out")
            g.add_edge(pydot.Edge(id_node, id_child))


            id_child = create_graph(g, dre)
            nodeDre = g.get_node(str(id_child))[0]
            nodeDre.set("ordering", "out")
            g.add_edge(pydot.Edge(id_node, id_child))

            return id_node
        
        case Abstraccio(lletra, terme):
            id_node = node_count
            node_count += 1
            g.add_node(pydot.Node(name=str(id_node), label="λ" + lletra, shape="none"))
            
            nou = True
            if lletra in parent:
                nou = False
                oldValue = parent[lletra]
            parent[lletra] = id_node

            id_child = create_graph(g, terme)
            g.add_edge(pydot.Edge(id_node, id_child))

            if nou:
                parent.pop(lletra)
            else:
                parent[lletra] = oldValue

            return id_node

        case str(s):
            id_node = node_count
            node_count += 1
            g.add_node(pydot.Node(name=str(id_node), label=s, shape="none"))
            if s in parent:
                g.add_edge(pydot.Edge(str(id_node), str(parent[s]), style="dotted"))
            return id_node


async def aval(update: Update, context):
    MAX_ITERACIONS = 75
    
    inp = update.message.text

    defmacro = '=' in inp or '≡' in inp
    (tree, parser) = parseInput(inp)
    try:
        if parser.getNumberOfSyntaxErrors() == 0:
            visitor = TreeVisitor()
            t = visitor.visit(tree)
            if not defmacro:
                await update.message.reply_text(string(t))
                graph = pydot.Dot(graph_type="digraph")
                create_graph(graph, t)
                graph.write_png('graph.png')
                await update.message.reply_photo('graph.png')
            

                trobat = [True]
                beta_red = t
                iteracions = 0
                while trobat[0] and iteracions < MAX_ITERACIONS:
                    trobat = [False]
                    t = beta_red
                    (beta_red, operacions) = beta_reduccio(beta_red, trobat)
                    for op in operacions:
                        if op[0] == "a":
                            await update.message.reply_text(op[1] + " →α→ " + op[2])
                        elif op[0] == "b":
                            await update.message.reply_text(op[1] + " →β→ " + op[2])
                            
                    if trobat[0] and string(t) == string(beta_red):
                        beta_red = "Nothing"
                        await update.message.reply_text("...")
                        break

                if iteracions >= MAX_ITERACIONS:
                    beta_red = "Nothing"
                    await update.message.reply_text("...")

                await update.message.reply_text(string(beta_red))
                graph = pydot.Dot(graph_type="digraph")
                create_graph(graph, beta_red)
                graph.write_png('graph.png')
                await update.message.reply_photo('graph.png')
        else:
            await update.message.reply_text('errors de sintaxi.')
    except MacroNoDefinit as error:
        await update.message.reply_text(str(error))

TOKEN = open('token.txt').read().strip()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, aval))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("author", author))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("macros", macrosF))

app.run_polling()