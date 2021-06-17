const { MessageEmbed } = require('discord.js');
module.exports = {
    name: "ping",
    description: "Informa ao ping",
    execute(message, args, client) {
        var ping = message.createdTimestamp - Date.now();
        const embed = new MessageEmbed()
            // Set the title of the field
            .setTitle('O Ping')
            // Set the color of the embed
            .setColor(0xff0000)
            // Set the main content of the embed
            .setDescription(" ping aqui ó `" + `${ping}` + " ms`");
        // Send the embed to the same channel as the message
        message.channel.send(embed);

    }
}