const {Client, MessageEmbed }= require("discord.js");
const client = new Client();
const express = require("express")
const app = express()
app.use(express.json())
const { token, prefix,port } = require("./config.json");
const PORT = port || 3000

let time = 10; //time do bot em minutes
let proxtime = 0;
client.on('message', message => {

    if (message.author.bot) return;
    if (message.channel.type === "dm") return;
    if (message.content.startsWith(prefix)) {
        const args = message.content.slice(prefix.length).split(/ +/);
        const comm = args.shift().toLowerCase();
        if (comm == 'timebot') message.channel.send(`${Math.floor((proxtime - Date.now()) / 60000)}`);

    }
});

const send_discord = (channel, content) => {
    const embed = new MessageEmbed()
      // Set the title of the field
      .setTitle(content.title)
      // Set the color of the embed
      .setColor(content.color)
      .addFields(
		{ name: 'Type', value: content.type },
        { name: 'Value', value: content.content },
	)
      // Set the main content of the embed
      .setDescription(content.description)
      .setTimestamp();

    client.channels.cache.forEach(channel_discord =>{
        if (channel_discord.id == channel) channel_discord.send(embed)
    })
}


app.post('/',(req,res) =>{
    send_discord(818475844770070529,req.body)
    res.send("Envia pro discord")
})

client.login(token)
app.listen(PORT, () => console.log("Startou na porta "+ PORT))

