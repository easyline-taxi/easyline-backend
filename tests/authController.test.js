const request = require("supertest");
const app = require("../src/app");
const User = require('../database/models/usersSchema')
const Point = require('../database/models/pointsSchema')

// describe("Test the root path", () => {
//   // jest.useFakeTimers()
//   test("It should response the GET method", done => {
//     request(app)
//       .get("/")
//       .then(response => {
//         expect(response.statusCode).toBe(200);
//         done();
//       });
//   });
// });


describe("Test /users/register", () => {
  jest.setTimeout(30000)
  let users = [
    {
      email: "fromtesteemail@email",
      deviceId: 12312312312,
      name: "User Test",
      password: "123",
      admin: false
    }
  ]

  beforeAll(async () => {
    await User.create(users[0]);
    console.log("Adicionando usuários")
  });

  afterAll(done => {
    // code to run before each test
    users.forEach(async user => {
      if(user.nameofpoint) await Point.deleteOne({name: user.nameofpoint})
      await User.deleteOne({ email: user.email })
    })
    console.log("Removendo usuários")
    done()
  });

  test("Registro de Campos Vazios", done => {

    request(app)
      .post("/users/register")
      .send()
      .expect(400)
      .end(done)
  })

  test("Register Valid User", done => {
    const user = {
      email: `fromtesteemail${Math.floor(Math.random() * 200000)}@email`,
      deviceId: Math.floor(Math.random() * 200000),
      name: "User Test Valid",
      password: "123",
      admin: false
    }
    users.push(user);

    request(app)
      .post("/users/register")
      .send(user)
      .set('Accept', 'application/json')
      .expect(200)
      .end(done)

  });

  test("Register Repeat Email", done => {
    const user = {
      email: users[0].email,
      deviceId: Math.floor(Math.random() * 200000),
      name: "User Test",
      password: "123",
      admin: false
    }

    request(app)
      .post("/users/register")
      .send(user)
      .set('Accept', 'application/json')
      .expect(400)
      .end(done)
  });

  test("Register without deviceId", done => {
    const user = {
      email: `fromtesteemail${Math.floor(Math.random() * 200000)}@email`,
      name: "User Test",
      password: "123",
      admin: false
    }

    request(app)
      .post("/users/register")
      .send(user)
      .set('Accept', 'application/json')
      .expect(400)
      .end(done)
      
  });

  test("Register repeat DeviceId",  done => {
    const user = {
      email: `fromtesteemail${Math.floor(Math.random() * 200000)}@email`,
      deviceId: users[0].deviceId,
      name: "User Test",
      password: "123",
      admin: false
    }
    request(app)
      .post("/users/register")
      .send(user)
      .expect(400)
      .end(done);
  })


  test("Register admin true without nameofpoint",  done => {
    const user = {
      email: `fromtesteemail${Math.floor(Math.random() * 200000)}@email`,
      deviceId: Math.floor(Math.random() * 200000),
      name: "User Test",
      password: "123",
      admin: true
    }
    request(app)
      .post("/users/register")
      .send(user)
      .expect(400)
      .end(done);
  })

  test("Register admin true with nameofpoint",  done => {
    const user = {
      email: `fromtesteemail${Math.floor(Math.random() * 200000)}@email`,
      deviceId: Math.floor(Math.random() * 200000),
      name: "User Test",
      password: "123",
      admin: true,
      nameofpoint: "Os Grandes Mestres"
    }
    users.push(user)
    request(app)
      .post("/users/register")
      .send(user)
      .expect(200)
      .end(done);
  })

});


describe("Test /users/login", () => {
  jest.setTimeout(30000)
})