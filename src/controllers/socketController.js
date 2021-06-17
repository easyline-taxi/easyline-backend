
var Logs = require('../../database/models/logSchema')
var bot = require('../../botComponents')
var {authTokenSimple} = require('../middlewares/authToken')
module.exports = {
    start: (socket) => {
        console.log("Start Executou")
        socket.on('connection', (sock) => {
            console.log("Usuário Conectado WebSocket")
            bot.sendMessage({title: "Usuário Conectado websocket", content: ""})
            // console.log(sock)
            // const last = new Logs({ service: "websocket", ip: sock.handshake.client, content: "Connectado" })
            // last.save((err, res) => { console.log(err) })
        });
    },
    disconnect: (socket) => {
        socket.on('disconnect', (sock) => {
            console.log("Usuário Desconectado WebSocket")
            bot.sendMessage({title: "Usuário Desconectado websocket", content: ""})
            // console.log(sock)
            
        })
    },
    message: (socket) =>{
        socket.on('message', sock => {
            bot.sendMessage({title: "Mensagem Websocket", content: sock})
        })
    } 

}