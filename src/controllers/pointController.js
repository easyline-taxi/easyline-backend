var User = require('../../database/models/usersSchema')
var Point = require('../../database/models/pointsSchema')
var { historic_utils, add_employee } = require('./utils')
const db = require('../../database/index')

const { bot } = require('./botController')


module.exports = {
    userAdd: async (req, res) => {
        let dataAdmin = req.userData
        const { email } = req.body
        if (!email) res.status(401).json({ message: "campo 'Email' é necessário" })
        // if (dataAdmin.email == req.body.email) return res.status(401).json({ message: "Não pode cadastrar seu próprio email!" })
        let motorista = await User.findOne({ email })
        if (!motorista)
            return res.status(404).json({ message: "Email Não Encontrado" })

        let ponto = await Point.findOne({ _id: dataAdmin.pointowner })
        if (!ponto) console.error("Inconsistência no ponto do admin")

        let filtred = ponto.employee.filter(cad => { if (String(motorista._id) == String(cad.id)) return cad })
        if (filtred.length > 0 && filtred[0].deviceId.toString() != motorista.deviceId.toString()) {
            console.log("O usuário tem q se cadastrar dnv")
            // remover do ponto qualquer que esteja (ok)
            let pontoCadastrado;
            if (motorista.registeredpoint)
                pontoCadastrado = Point.findById(motorista.registeredpoint)
            let filtred = pontoCadastrado.employee.filter(emp => emp.email != motorista.email)
            pontoCadastrado.employee = filtred
            pontoCadastrado.historic.push(historic_utils("sair", motorista._id, `${motorista.email} saiu do ponto ${pontoCadastrado.name}`))
            pontoCadastrado.markModified('historic')
            pontoCadastrado.markModified('employee')
            // atualizar o deviceId
            motorista.deviceId = deviceId
            motorista.registeredpoint = null
            motorista.historic.push(historic_utils("saiu", ponto._id, `Saiu do ponto ${ponto.name} devido deviceId diferente`))
            motorista.markModified('historic')
            try {
                pontoCadastrado.save()
                motorista.save()
                console.log("Usuário saiu do antigo ponto")
            } catch (ex) {
                return res.status(400).send({ message: "Erro em remover dados no bd", erro: e })
            }
            // Cadastrar normalmente
        } else {
            if (filtred.length > 0) return res.status(401).json({ message: "Email já Cadastrado nesse ponto" })
            if (motorista.registeredpoint) return res.status(401).json({ message: "Motorista já possui ponto cadastrado!" })
        }

        ponto.employee.push(add_employee(motorista._id, motorista.name, motorista.email, motorista.vtr, motorista.deviceId, "motorista"))
        ponto.historic.push(historic_utils("adicionar", motorista._id, `${motorista.email} foi adicionado pelo ${dataAdmin.email}`))
        ponto.markModified('employee');
        ponto.markModified('historic');

        dataAdmin.historic.push(historic_utils("adicionar", motorista._id, `Adicionou ${motorista.email} no ponto ${ponto.name}`))
        dataAdmin.markModified('historic');

        motorista.registeredpoint = db.Types.ObjectId(ponto._id)
        motorista.historic.push(historic_utils("adicionar", ponto._id, `Foi adicionado no ponto ${ponto.name} pelo ${dataAdmin.email}`))
        motorista.markModified('historic');

        try {
            ponto.save()
            motorista.save()
            dataAdmin.save()
            bot.sendMessage({ title: "Adicionado como Motorista", content: `Admin:${dataAdmin.email}\n Usuário: ${motorista.email}` })
            res.status(200).send({ message: "Adicionado como Motorista" })
        } catch (e) {
            res.status(400).send({ message: "Erro no salvamento dos dados ao adicionar usuário", erro: e })
        }
    },
    userDel: async (req, res) => {
        let dataAdmin = req.userData
        const { email, motivo } = req.body
        if (!email) return res.status(401).json({ message: "Post Inválido" })
        if (!motivo) motivo = "nenhum"
        // if (dataAdmin.email == email) return res.status(401).json({ message: "Não pode deletar seu próprio email!" })
        var ponto = await Point.findOne({ _id: dataAdmin.pointowner })
        let filtred = ponto.employee.filter(mot => { if (mot.email == email) return mot })
        if (!filtred.length) return res.status(401).json({ message: "Motorista Não Cadastrado neste ponto" })
        let motorista = await User.findOne({ email })

        ponto.employee = ponto.employee.filter(mot => { if (mot.email != email) mot })
        ponto.historic.push(historic_utils("remover", motorista._id, motivo))
        ponto.markModified('historic')
        ponto.markModified('employee')

        dataAdmin.historic.push(historic_utils("remover", motorista._id, `Removeu ${motorista.email} do ponto ${ponto.name} pelo motivo '${motivo}'`))
        dataAdmin.markModified('historic')

        motorista.registeredpoint = null
        motorista.historic.push(historic_utils("remover", ponto._id, `Removido do ponto ${ponto.name} pelo motivo '${motivo}'`))
        motorista.markModified('historic')

        try {
            ponto.save()
            dataAdmin.save()
            motorista.save()
            bot.sendMessage({ title: "Usuário removido Com Sucesso", content: `Usuário:${motorista.name}\nPonto: ${ponto.name}\nMotivo ${motivo}` })
            res.status(200).json({ message: "Usuario removido com sucesso" })
        } catch (e) {
            res.status(400).send({ message: "Erro no salvamento dos dados ao remover usuário", erro: e })
        }
    },
    changeOwner: () => {

    },
    newPoint: () => {
        // aqui o cara vai virar admin

    },
    deletePoint: () => {

    },
    findInconsistences: async (req, res) => {
        let inconsistencias = 0, complete = 0;

        let points = await Point.find();
        // checar locals e funcionarios
        bot.sendMessage({ title: "Começando a Procura por Inconsistências", content: `Procurando... ${complete}%` })
        if (points.length == 0) return res.status(200).json({ message: "Não há pontos" })
        await points.forEach(point => {
            console.warn(`Ponto ${point.name}`)
            point.employee.forEach(async emps => {
                let emp = await User.findById(emps.id)
                if (emp.registeredpoint.toString() != point._id.toString()) {
                    await console.error(`Ponto ${point.name} encontrado`)
                    bot.sendMessage({ title: "Inconsistencia Encontrada!", content: `ponto ${point.name} registrado com ${emp.email} mas não o constrário` })
                    await inconsistencias++;
                    try {
                        emp.registeredpoint = point._id
                        await emp.save()
                        bot.sendMessage({ title: "Correção Inconsistência", content: `Dados user ${emp.email} foram recolocados novamente!` })
                    } catch (err) {
                        bot.sendMessage({ title: "Erro na correção", content: `Dados user ${emp.email} continuam inconsistentes!\nerro: ${err}` })
                    }
                }
            })
        })
        let users = await User.find()
        if (points.length == 0) return res.status(200).json({ message: "Não há usuários" })
        await users.forEach(async user => {
            console.warn(`User ${user.email} `)

            if (!user.registeredpoint) return
            let point = await Point.findById(user.registeredpoint)
            if (!point) {
                await inconsistencias++;
                bot.sendMessage({ title: "Inconsistencia Encontrada!", content: `user ${user.email} possui ponto inexistente cadastrado!` })
                try {
                    user.registeredpoint = null
                    bot.sendMessage({ title: "Correção Inconsistência", content: `Dados relacionado aos pontos do user ${user.email} foram removidos!` })
                    await user.save()
                } catch (err) {
                    bot.sendMessage({ title: "Erro na correção", content: `Dados user ${user.email} continuam inconsistentes!\nerro: ${err}` })
                }

            }
            let filtred = point.employee.filter(emp => emp.id.toString() == user._id.toString())
            if (filtred.length == 0) {
                console.error(`User ${user.email} encontrado`)
                await inconsistencias++;
                bot.sendMessage({ title: "Inconsistencia Encontrada!", content: `user ${user.email} registrado ${point.name} mas não o constrário` })
                try {
                    user.registeredpoint = null
                    bot.sendMessage({ title: "Correção Inconsistência", content: `Dados relacionado aos pontos do user ${user.email} foram removidos!` })

                    await user.save()
                } catch (err) {
                    bot.sendMessage({ title: "Erro na correção", content: `Dados user ${user.email} continuam inconsistentes!\nerro: ${err}` })
                }

            }
        })

        res.send("OK")


    }
}