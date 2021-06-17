const mongoose = require('../index');

const logSchema = new mongoose.Schema({
    service: String,
    target: String,
    ip: String,
    content: Array,
    params: Array,
    response: Map,
    date: { type: Date, default: new Date(new Date().valueOf() - new Date().getTimezoneOffset() * 60000) },
    createdAt: {type:Date, default: Date.now, index: { expires: 60*24*15 }}
}, { timestamps: true })

const Logs = mongoose.model('logs', logSchema)
module.exports = Logs