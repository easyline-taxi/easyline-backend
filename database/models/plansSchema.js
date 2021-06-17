const mongoose = require('../index');

const plansSchema = new mongoose.Schema({
    name:{type: String, required: true, unique: true},
    value:{type: Number,default:null},
    date: { type: Date, default:  new Date(new Date().valueOf()- new Date().getTimezoneOffset() * 60000)},
})

const Plans = mongoose.model('plans', plansSchema)
module.exports = Plans