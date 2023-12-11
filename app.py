import json
import quart
import quart_cors
from quart import request

# Crear la aplicación Quart con CORS habilitado
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://usersapi2.azurewebsites.net")

# Diccionario para almacenar las tareas (to-dos) por usuario
_TODOS = {}

# Endpoint para añadir una tarea
@app.post("/todos/<string:username>")
async def add_todo(username):
    data = await request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(data["todo"])
    return quart.Response(response='OK', status=200)

# Endpoint para obtener tareas de un usuario
@app.get("/todos/<string:username>")
async def get_todos(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

# Endpoint para eliminar una tarea específica de un usuario
@app.delete("/todos/<string:username>")
async def delete_todo(username):
    data = await request.get_json(force=True)
    todo_idx = data["todo_idx"]
    if 0 <= todo_idx < len(_TODOS.get(username, [])):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

# Endpoint para servir el logo
@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

# Endpoint para servir el manifiesto del plugin
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("ai-plugin.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", "https://usersapi2.azurewebsites.net")
        return quart.Response(text, mimetype="text/json")

# Endpoint para servir la especificación OpenAPI
@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", "https://usersapi2.azurewebsites.net")
        return quart.Response(text, mimetype="text/yaml")

# Función principal para ejecutar la aplicación
def main():
    app.run(debug=True, host="0.0.0.0", port=5002)

if __name__ == "__main__":
    main()
