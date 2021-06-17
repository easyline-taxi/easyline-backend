const { MessageEmbed } = require('discord.js');
const Logs = require('./../../database/models/logSchema')
module.exports = {
    name: "logs",
    description: "Informa os logs: <>",
    execute(message, args, client) {
        if (args[0]) {
            try {
                args = parseInt(args[0])
                Logs.find().sort({ 'date': 1 }).limit(args).then(res => {
                    if (res.length) {
                        res.map(log => {
                            const embed = new MessageEmbed()
                                // Set the title of the field
                                .setTitle(`Logs: ${new Date(log.date).toGMTString()}`)
                                // Set the color of the embed
                                .setColor(0xffffff)
                                // Set the main content of the embed
                                .setDescription(`${log}`);
                            // Send the embed to the same channel as the message
                            message.channel.send(embed);
                        })

                    } else {
                        const embed = new MessageEmbed()
                            // Set the title of the field
                            .setTitle(`Não há logs disponíveis`)
                            // Set the color of the embed
                            .setColor(0xffffff)
                            // Set the main content of the embed
                            .setDescription(`Tente alguma ação na API`);
                        // Send the embed to the same channel as the message
                        message.channel.send(embed);
                    }
                })

            } catch (e) {
                const embed = new MessageEmbed()
                    // Set the title of the field
                    .setTitle("Argumento não numeral: " + "'tente !logs <inteiro>'")
                    // Set the color of the embed
                    .setColor(0xff0000)
                    // Set the main content of the embed
                    .setDescription(`${e}`);
                // Send the embed to the same channel as the message
                message.channel.send(embed);
            }
        } else {
            Logs.find().sort({ 'date': 1 }).limit(1).then(res => {
                if (res.length) {
                    res.map(log => {
                        const embed = new MessageEmbed()
                            // Set the title of the field
                            .setTitle(`Logs: ${new Date(log.date).toGMTString()}`)
                            // Set the color of the embed
                            .setColor(0xffffff)
                            // Set the main content of the embed
                            .setDescription(`${log}`)
                            .addField("Apenas o log mais atual","Nothing")
                        // Send the embed to the same channel as the message
                        message.channel.send(embed);

                    })

                } else {
                    const embed = new MessageEmbed()
                        // Set the title of the field
                        .setTitle(`Não há logs disponíveis`)
                        // Set the color of the embed
                        .setColor(0xffffff)
                        // Set the main content of the embed
                        .setDescription(`Tente alguma ação na API`);
                    // Send the embed to the same channel as the message
                    message.channel.send(embed);
                }
            })
        }





    }
}