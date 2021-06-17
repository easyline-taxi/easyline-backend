const { MessageEmbed } = require('discord.js');
const Bot = require('./../../database/models/botSchema')


module.exports = {
    name: "activate",
    description: "Ativa o bot",
    async execute(message, args, client) {
        let botStatus = await Bot.findOne()
        console.log(botStatus)
        if (!botStatus) botStatus = await Bot.create()

        if (!botStatus.online) {
            botStatus.online = true;
            try {

                await botStatus.save()

                const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("Solicitação de Ativação")
                    .setAuthor(client.user.username, client.user.avatarURL)

                    // Set the color of the embed
                    .setColor("#f44d43")
                    // Set the main content of the embed
                    .setDescription("Ativando.... Pronto!!")
                    .setTimestamp()
                message.channel.send(embed)
            } catch (err) {
                const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("ERRO: Solicitação de Ativação")
                    .setAuthor(client.user.username, client.user.avatarURL)

                    // Set the color of the embed
                    .setColor("#f44d43")
                    // Set the main content of the embed
                    .setDescription(err)
                    .setTimestamp()
                    message.channel.send(embed)

            }
        }
        else {
            const embed = new MessageEmbed()
                // Set the title of the field
                .setTitle("Solicitação de Ativação")
                .setAuthor(client.user.username, client.user.avatarURL)

                // Set the color of the embed
                .setColor("#f44d43")
                // Set the main content of the embed
                .setDescription("Eu já estou ativo!!")
                .setTimestamp()
                message.channel.send(embed)
        }
    }

}
