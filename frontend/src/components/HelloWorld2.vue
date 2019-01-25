<template>
  <div class="hello">
    <div class="card" style="float:left">
      <h1><img v-if="this.weather==0" src="../assets/sun.png" width="50" height="50" >
        <img v-if="this.weather==1" src="../assets/cloud.png" width="50" height="50"> {{data[0]}} ºC</h1>
      {{data[1]}} <br/>
      {{data[2]}} <br/>
    </div>
      {{data[3]}} :{{data[4]}}<br>
      {{data[5]}} :{{data[6]}}<br>
      {{data[7]}} :{{data[8]}}<br>
      오전 강수확률{{data[9]}}% <br/>
      오후 강수확률{{data[10]}}% <br/>
      실내 기온{{data2[0]}}도<br/>
      실내 습도{{data2[1]}}%<br/>
      실내 미세먼지{{data3[0]}}ug/m<br>
      실내 초미세먼지{{data3[1]}}ug/m<br>
    </div>
    <img id="photo" src="../../../img/download1.jpg" width="150" height="150">
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  sockets: {
    connect: function(){
      console.log('socket connected')
    },
    mise: function(a){
      console.log('get mise')
      console.log(a)
      this.data = a.data
    },
    inside: function(b){
      console.log('get inside')
      console.log(b)
      this.data2 = b.data
    },
    insidedust: function(c) {
      console.log('get inside dust')
      console.log(c)
      this.data3 = c.data
    }
  },
  props: {
    msg: String
  },
  data () {
    return {
      data: null,
      data2: null,
      data3: null,
      weather: 0
    }
  },
  mounted: function() {
    console.log('in mounted')
    this.getInfo()
  },
  methods: {
    getInfo: function(){
      this.$socket.emit('mise')
      console.log('getMise called')
      this.$socket.emit('inside')
      console.log('getInside called')
      this.$socket.emit('insidedust')
      console.log('getInsideDust called')
    },
    getImg: function(){
      if(this.data[1]=='흐림'){
        this.weather = 1
      }


    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello{
  font-weight: 300;
  padding-bottom: 700px;
}
#card2{
  padding-top: 50px;
  font-size: 15px;
}
#photo{
  left :0;
  padding-left: 10px;
  padding-bottom: 10px;

}
h1 {
  font-weight: 500;
}
h2{
  font-weight: 500;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
a {
  color: #42b983;
}
</style>
