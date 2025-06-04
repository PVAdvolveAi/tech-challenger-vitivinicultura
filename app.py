from flask import Flask, jsonify, abort, request
from flasgger import Swagger, swag_from
from scraper import carregar_aba_por_csv
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# ---------- Configurações de JWT ----------
# troque por algo robusto
app.config["JWT_SECRET_KEY"] = "tech_challenge01"
jwt = JWTManager(app)

# ---------- Configuração do Swagger + JWT (bearerAuth) ----------
template = {
    "swagger": "2.0",
    "info": {
        "title": "API Vitivinicultura Embrapa",
        "version": "1.0",
        "description": "Documentação gerada pelo Flasgger + JWT"
    },
    # Definimos explicitamente a ordem de exibição dos grupos:
    "tags": [
        {"name": "default",
            "description": "Endpoints padrão (Home, Documentação)"},
        {"name": "Auth",             "description": "Autenticação e emissão de token"},
        {"name": "Produção",         "description": "Dados de Produção da Embrapa"},
        {"name": "Processamento",    "description": "Dados de Processamento da Embrapa"},
        {"name": "Comercialização",
            "description": "Dados de Comercialização da Embrapa"},
        {"name": "Importação",       "description": "Dados de Importação da Embrapa"},
        {"name": "Exportação",       "description": "Dados de Exportação da Embrapa"}
    ],
    "securityDefinitions": {
        "bearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Use: Bearer <seu_token_JWT>"
        }
    }
}

app.config['SWAGGER'] = {'uiversion': 3}
swagger = Swagger(app, template=template)


# ---------- ROTA DE LOGIN (emite JWT) ----------
@app.route("/login", methods=["POST"])
def login():
    """
    Login para obter token JWT.
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Retorna access_token
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Falta JSON ou campos
      401:
        description: Credenciais inválidas
    """
    if not request.is_json:
        return jsonify({"msg": "Falta JSON"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "username e password são obrigatórios"}), 400

    # Exemplo fixo de usuário: em produção, valide em banco
    if username == "admin" and password == "senha123":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Credenciais inválidas"}), 401


# ---------- PÁGINA INICIAL (entra em “default”) ----------
@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>API Vitivinicultura Embrapa</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
            }
            h1 { color: #333; }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #0066CC;
                font-size: 18px;
            }
            a:hover {
                text-decoration: underline;
            }
            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>API Vitivinicultura Embrapa</h1>
        <p>Para acessar os dados (Produção, Processamento, etc.), siga estes passos:</p>
        <ol>
          <li>Faça <strong>POST /login</strong> para obter seu <em>access_token</em> (JWT).</li>
          <li>Acesse <a href="/documentacao">Documentação</a> (Swagger UI).</li>
          <li>No Swagger, clique em <strong>Authorize</strong> e cole <code>Bearer &lt;seu_token&gt;</code>.</li>
          <li>Use “Try it out” em cada rota (Produção, Processamento, Comercialização, Importação e Exportação).</li>
        </ol>
        <p>Ou seja, clique em <a href="/documentacao">Documentação</a> e autorize com seu token antes de testar as rotas.</p>
        <div class="footer">
            <p>Desenvolvido para o Tech Challenger – API em Flask</p>
        </div>
    </body>
    </html>
    """, 200


# ---------- PÁGINA DE DOCUMENTAÇÃO (entra em “default”) ----------
@app.route("/documentacao", methods=["GET"])
def documentacao():
    """
    Página que exibe o Swagger UI dentro de um iframe menor.
    ---
    responses:
      200:
        description: Exibe o Swagger UI em tamanho reduzido.
    """
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>Documentação da API</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 20px;
          background-color: #f0f0f0;
        }
        h1 {
          color: #333;
        }
        .iframe-container {
          width: 80%;
          max-width: 900px;
          margin: auto;
          border: 1px solid #ccc;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .iframe-container iframe {
          width: 100%;
          height: 600px;
          border: none;
        }
        a.back {
          display: inline-block;
          margin-top: 20px;
          text-decoration: none;
          color: #0066CC;
        }
        a.back:hover {
          text-decoration: underline;
        }
      </style>
    </head>
    <body>
      <h1>Documentação da API</h1>
      <p>Abaixo está o Swagger UI incorporado:</p>
      <div class="iframe-container">
        <iframe src="/apidocs"></iframe>
      </div>
      <p><a class="back" href="/">← Voltar ao menu principal</a></p>
    </body>
    </html>
    """, 200


# ---------- ROTAS DE DADOS (protegidas por JWT) ----------

@app.route("/producao", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Produção'],
    'security': [{'bearerAuth': []}],
    'responses': {
        200: {
            'description': 'Lista de registros de produção',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'categoria': {'type': 'string'},
                                'ano': {'type': 'integer'},
                                'valor': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token ausente ou inválido'},
        500: {'description': 'Erro interno ao obter dados'}
    }
})
def get_producao():
    """
    Obtém dados de Produção (opt_02)
    """
    try:
        df = carregar_aba_por_csv(2)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return abort(500, description=str(e))


@app.route("/processamento", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Processamento'],
    'security': [{'bearerAuth': []}],
    'responses': {
        200: {
            'description': 'Lista de registros de processamento',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'categoria': {'type': 'string'},
                                'ano': {'type': 'integer'},
                                'valor': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token ausente ou inválido'},
        500: {'description': 'Erro interno ao obter dados'}
    }
})
def get_processamento():
    """
    Obtém dados de Processamento (opt_03)
    """
    try:
        df = carregar_aba_por_csv(3)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return abort(500, description=str(e))


@app.route("/comercializacao", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Comercialização'],
    'security': [{'bearerAuth': []}],
    'responses': {
        200: {
            'description': 'Lista de registros de comercialização',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'categoria': {'type': 'string'},
                                'ano': {'type': 'integer'},
                                'valor': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token ausente ou inválido'},
        500: {'description': 'Erro interno ao obter dados'}
    }
})
def get_comercializacao():
    """
    Obtém dados de Comercialização (opt_04)
    """
    try:
        df = carregar_aba_por_csv(4)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return abort(500, description=str(e))


@app.route("/importacao", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'security': [{'bearerAuth': []}],
    'responses': {
        200: {
            'description': 'Lista de registros de importação',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'categoria': {'type': 'string'},
                                'ano': {'type': 'integer'},
                                'valor': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token ausente ou inválido'},
        500: {'description': 'Erro interno ao obter dados'}
    }
})
def get_importacao():
    """
    Obtém dados de Importação (opt_05)
    """
    try:
        df = carregar_aba_por_csv(5)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return abort(500, description=str(e))


@app.route("/exportacao", methods=["GET"])
@jwt_required()
@swag_from({
    'tags': ['Exportação'],
    'security': [{'bearerAuth': []}],
    'responses': {
        200: {
            'description': 'Lista de registros de exportação',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'categoria': {'type': 'string'},
                                'ano': {'type': 'integer'},
                                'valor': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token ausente ou inválido'},
        500: {'description': 'Erro interno ao obter dados'}
    }
})
def get_exportacao():
    """
    Obtém dados de Exportação (opt_06)
    """
    try:
        df = carregar_aba_por_csv(6)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return abort(500, description=str(e))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
