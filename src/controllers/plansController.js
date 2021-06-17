var Plans = require('../../database/models/plansSchema')

module.exports = {
    change: async(req, res) => {
        
        res.status(200).json({ message: "Autenticado", result: {_id, nomedoponto, nome, senha, plano, cidade, estado, numeroVTR,funcionarios,historico } })
    },
    create: async(req, res) => {
        
        res.status(200).json({ message: "Autenticado", result: {_id, nomedoponto, nome, senha, plano, cidade, estado, numeroVTR,funcionarios,historico } })
    }
}