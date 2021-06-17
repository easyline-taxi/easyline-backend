
const Discord = require('discord.js');
const client = new Discord.Client();
const fs = require('fs');
const { prefix, token } = require('./config/config.json');


client.commands = new Discord.Collection();

const commandFiles = fs.readdirSync(__dirname + '/commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const command = require(__dirname + `/commands/${file}`);
    client.commands.set(command.name, command);
}

client.sendSemAuth = (message) => {
    console.log("Ainda não Está disponível")
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

client.on('ready', () => {

    sendSemAuth = (message, channel = '817168297648193637') => {
        let local = client.channels.cache.get(channel)

        local.send(message)
    }

    client.sendSemAuth = sendSemAuth;
    console.log('Pronto!');
})

client.on('message', message => {
    if (message.author.bot) return;
    if (message.channel.type === 'dm') return;
    if (message.content.startsWith(prefix)) {
        const args = message.content.slice(prefix.length).split(/ +/);
        const command1 = args.shift().toLowerCase();
        try {
            client.commands.get(command1).execute(message, args, client);
        } catch (error) {
            // comando incorreto
        }
    }

});
client.login(token);

module.exports = client

module.exports.middleware = async (req, res, next) => {
    try {
        const embed = new Discord.MessageEmbed()
            // Set the title of the field
            .setTitle("Request " + req.method || "Empty")
            .setAuthor(client.user.username, client.user.avatarURL)

            // Set the color of the embed
            .setColor(getRandomColor())
            // Set the main content of the embed
            .addField("From", req.ip || "Empty", true)
            .addField("To", req.originalUrl || "Empty", true)
            .addField("Body Params", Object.keys(req.body).length ? Object.keys(req.body) : "Empty")
            .setTimestamp()

        client.sendSemAuth(embed, "818475844770070529")

    } catch (e) {

    }

    // console.log(req)
    next();
}

module.exports.sendMessage = async (message) => {
    const embed = new Discord.MessageEmbed()
        // Set the title of the field
        .setTitle(message.title)
        .setAuthor(client.user.username, client.user.avatarURL)

        // Set the color of the embed
        .setColor("#f44d43")
        // Set the main content of the embed
        .setDescription(message.content)

        .setTimestamp()

    client.sendSemAuth(embed, "818475844770070529")
}

module.exports.MessageEmbed = new Discord.MessageEmbed()