const { Manager } = require("socket.io-client");


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1cs2VybmFtZSI6Indlc2xleWJlbmljaW81QGdtYWlsLmNvbSIsImV4cCI6MTY0ODgxNzYyNiwiZW1haWwiOiJ3ZXNsZXliZW5pY2lvNUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTY0ODY0NDgyNn0.PmF9pGcH32Jsguvq1eIUVKV3E1Cn0aq01nHJ5MwhDxw"
const manager = new Manager("ws://127.0.0.1:8888", {
    reconnectionDelayMax: 10000
});
manager.open((err) => {
    if (err) {
        console.error("Erro: ", err)
    } else {
        console.log("the connection was successfully established")
    }
});
const socket = manager.socket("/row", {
    auth: token
});

socket.on("error", (error) => {
    console.error("Erro /row: ", error)
})

socket.io.on("reconnect", (attempt) => {
    console.error("Reconexão /row: ", attempt)
});

socket.on("location_updated", (...args) => {
    console.log("EVENTO RECEBIDO: location_updated")
});

socket.on("row_update", (...args) => {
    console.log("EVENTO RECEBIDO: row_update")
});

socket.on("connect", () => {
    const engine = socket.io.engine;
    console.log(engine.transport.name); // in most cases, prints "polling"

    engine.once("upgrade", () => {
        // called when the transport is upgraded (i.e. from HTTP long-polling to WebSocket)
        console.log(engine.transport.name); // in most cases, prints "websocket"
    });

    engine.on("packet", ({ type, data }) => {
        // called for each packet received
    });

    engine.on("packetCreate", ({ type, data }) => {
        // called for each packet sent
    });

    engine.on("drain", () => {
        // called when the write buffer is drained
    });

    engine.on("close", (reason) => {
        // called when the underlying connection is closed
        console.log("Conexão Fechada")
    });
});

setInterval(() => {
    console.log("Emitindo Evento: ",socket.connected)
    socket.emit("set_location", {
        "coordinate": {
            "latitude": 0,
            "longitude": 0
        }
    });
}, 2000)
