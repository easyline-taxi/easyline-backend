const { MessageEmbed } = require('discord.js');
const Bot = require('../../database/models/botSchema')


module.exports = {
    name: "deactivate",
    description: "desativa o bot",
    async execute(message, args, client) {
        let botStatus = await Bot.findOne()
        if (botStatus.online) {
            botStatus.online = false;
            try {
                await botStatus.save()

                const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("Solicitação de Desativação")
                    .setAuthor(client.user.username, client.user.avatarURL)

                    // Set the color of the embed
                    .setColor("#f44d43")
                    // Set the main content of the embed
                    .setDescription("Desativando.... Pronto!!")
                    .setTimestamp()
                message.channel.send(embed)
            } catch (err) {
                const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("ERRO: Solicitação de Desativação")
                    .setAuthor(client.user.username, client.user.avatarURL)

                    // Set the color of the embed
                    .setColor("#f44d43")
                    // Set the main content of the embed
                    .setDescription(err)
                    .setTimestamp()
               message.channel.send(embed)
            }

        }else{
            const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("Solicitação de Desativação")
                    .setAuthor(client.user.username, client.user.avatarURL)

                    // Set the color of the embed
                    .setColor("#f44d43")
                    // Set the main content of the embed
                    .setDescription("Já estou desativado!")
                    .setTimestamp()
                message.channel.send(embed)
        }
    }

}
