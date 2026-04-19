from app.main import create_app
from app.config.settings import settings
from gRPC.grpc_server import start_grpc_server

app = create_app()

if __name__ == "__main__":
    grpc_server = start_grpc_server()
    app.run(host=settings.HOST, port=settings.PORT, debug=False)
    grpc_server.wait_for_termination()
