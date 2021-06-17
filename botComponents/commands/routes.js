const { MessageEmbed } = require('discord.js');
module.exports = {
    name: "routes",
    description: "Informa os Endpoints",
    execute(message, args, client) {
        const embed = new MessageEmbed()
            // Set the title of the field
            .setTitle('Rotas Dinamicamente Encontradas na API')
            // Set the color of the embed
            .setColor(0xff0000)
            // Set the main content of the embed
            .addFields(client.routes.length ? client.routes.map(val =>{
                return {name: val.split(' ')[0], value: val.split(' ')[1]}
            }) : "/" )
        // Send the embed to the same channel as the message
        message.channel.send(embed);

    }
}