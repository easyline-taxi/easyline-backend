const mongoose = require('../index');

const users = new mongoose.Schema({
    email: { type: String, unique: true, required: true },
    deviceId: { type: String, unique: true, required: true },
    name: { type: String, required: true },
    password: { type: String, required: true },
    city: { type: String, default: null },
    country: { type: String, default: null },
    vtr: { type: Number, default: null },
    registeredpoint: {type: mongoose.Types.ObjectId, default: null, ref:'points'},
    pointowner: { type: mongoose.Types.ObjectId, default: null, ref:'points'},
    historic: { type: Array, default: [] },
    date: { type: Date, default: new Date(new Date().valueOf() - new Date().getTimezoneOffset() * 60000) },
}, { timestamps: true })

const Logs = mongoose.model('users', users)
module.exports = Logs