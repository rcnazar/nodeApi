let chai = require('chai');
let chaiHttp = require('chai-http');
//let should = chai.should();
let server = require.main.require('index');

chai.use(chaiHttp);

describe('Carros', () => {
    describe('/GET carros', () => {
        it('deve retornar todos os carros', (done) => {
            chai.request(server)
                .get('/carros')
                .set('token', '123')
                .end((err, res) => {
                    console.log(res.body);
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    //res.body.length.should.be.eql(0);
                    done();
                });          
        });
        it('deve retornar 403 quando sem autorização', (done) => {
            chai.request(server)
                .get('/carros')
                .end((err, res) => {
                    res.should.have.status(403);
                    done();
                });
        });
    });
});