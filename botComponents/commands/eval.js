const { MessageEmbed } = require('discord.js');
const beautify = require("js-beautify");
module.exports = {
    name: "eval",
    description: "Executa comando server",
    execute(message, args, client) {
        if (!args[0]) return message.reply("❌ | **Você precisa digitar algum comando!**").then(x => x.delete({ timeout: 5000 }));

        try {
            if (args.join(" ").toLowerCase().includes("token")) return;

            const toEval = args.join(" ");
            const evaluated = eval(toEval);

            let embed = new MessageEmbed()
                .setTimestamp()
                .setTitle("Resultado avaliado")
                .addField("Entrada: ", `\`\`\`js\n${beautify(args.join(" "), { format: "js" })}\n\`\`\``)
                .addField("Retorno: ", evaluated)
                .addField("Tipo: ", typeof (evaluated));

            message.channel.send(embed);

        } catch (e) {
            let embed = new MessageEmbed()
                .setTitle("❌ Um erro ocorreu!")
                .setDescription(e)
            message.channel.send(embed);
        }
    }

}
