var obot;
var Bot = require('../../database/models/botSchema')

const activate_deactivate = async () => {
    let botStatus = await Bot.findOne()
    return botStatus.online
}

module.exports = {
    erroSend: async (err, req, res, next) => {
        //mantenha!!
        if (await activate_deactivate()) {
            obot = require('../../botComponents')
        } else return

        //pode mudar
        const embed = obot.MessageEmbed
            // Set the title of the field
            .setTitle("Ops Erro " + err.status || "500")
            .setAuthor(obot.user.username, obot.user.avatarURL)

            // Set the color of the embed
            .setColor("#f44d43")
            // Set the main content of the embed
            .setDescription(err.message)
            .addFields(
                { name: 'Origin', value: req.headers['x-forwarded-for'] || req.connection.remoteAddress },
                { name: 'Service', value: req.method },
                { name: 'IP', value: req.headers.host, inline: true },
                { name: 'Target', value: req.originalUrl, inline: true }
            )
            .setTimestamp()

        obot.sendSemAuth(embed, "818475844770070529")


        //mantenha!!
        try{
            obot= null
        }catch(e){

        }        
    },
    bot: {
        sendMessage: async (message) => {
            //mantenha!!
            if (await activate_deactivate()) {
                obot = require('../../botComponents')
            } else return

            obot?.sendMessage(message)

            //mantenha!!
            obot= null
        },
        setRoutes: async (routes) => {
            //mantenha!!
            if (await activate_deactivate()) {
                obot = require('../../botComponents')
            } else return
            obot.routes = routes
            //mantenha!!
            try{
                obot= null
            }catch(e){
    
            }  
        }
    }
}