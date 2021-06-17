const mongoose = require('../index');

const pointsSchema = new mongoose.Schema({
    name:{type: String, required: true, unique: true},
    plan:{type: mongoose.Types.ObjectId, default: mongoose.Types.ObjectId("605c824aaedba503b090b79a"), ref:'plans'},
    owner:{type: mongoose.Types.ObjectId,required:true},
    local:{type: Object, default:null},
    employee: { type: Array, default: [] }, // id, name, eamil, vtc, function, deviceID
    historic:{type: Array, default:[]},
    stack:{type: Object, default: null},
    PA: {type:Number,default:30}, // em KM
    date: { type: Date, default:  new Date(new Date().valueOf()- new Date().getTimezoneOffset() * 60000)},
})

const Points = mongoose.model('points', pointsSchema)
module.exports = Points