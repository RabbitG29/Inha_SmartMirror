<template>
  <div class="hello">
    <div class="">
      <h1>{{data4[0]}}년 {{data4[1]}}월 {{data4[2]}}일
      <br>
      <a v-if="data4[3]<10">0</a>{{data4[3]}}:<a v-if="data4[4]<10">0</a>{{data4[4]}}:<a v-if="data4[5]<10">0</a>{{data4[5]}}</h1>
    </div>
    <br/>
    <div class="card" id="card2" style="float:left">
      <h3>실외 정보</h3>
      {{data[3]}} : {{data[4]}}<br>
      {{data[5]}} : {{data[6]}}<br>
      {{data[7]}} : {{data[8]}}<br>
      오전 강수확률{{data[9]}}% <br/>
      오후 강수확률{{data[10]}}% <br/>
    </div>
     <div class="card" id="card4" style="float:right">
        <h1><img v-if="this.weather==0" src="../assets/sun.png" width="50" height="50" >
        <img v-if="this.weather==1" src="../assets/cloud.png" width="50" height="50"> {{data[0]}} ºC</h1>
        <h1>{{data[1]}}</h1>
        {{data[2]}} <br/>
    </div>
    <div class="card" id="card3" style="font-size : 20px; font-weight : lighter; text-align:left;">
      <h3>실내 정보</h3>
       기온{{data2[0]}}도<br/>
       습도{{data2[1]}}%<br/>
       미세먼지{{data3[0]}}ug/m<br>
       <a v-if="data3[0]<=30">좋음</a>
       <a v-else-if="data3[0]<=80">보통</a>
       <a v-else-if="data3[0]<=150">나쁨</a>
       <a v-else>매우 나쁨</a>
       <br>
       초미세먼지{{data3[1]}}ug/m<br>
       <a v-if="data3[1]<=15">좋음</a>
       <a v-else-if="data3[1]<=50">보통</a>
       <a v-else-if="data3[1]<=100">나쁨</a>
       <a v-else>매우 나쁨</a>
    </div>

<!--    <img id="photo" src="../../../img/download1.jpg" width="150" height="150">-->
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
      if(this.data[1]=='흐림') {
        this.weather=1;
      }
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
    },
    date: function(d){
      console.log('get inside date')
      console.log(d)
      this.data4 = d.data
      if(this.data4[5]==30) {
        this.$router.push({
          name: 'Second'
        })
      }
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
      data4: null,
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
      this.$socket.emit('date')
      console.log('getDate called')
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
@font-face{font-family: 'netmarbleM'; src:url('../fonts/netmarbleM.ttf')}
.hello{
  font-family: 'netmarbleM';
  font-weight: 300;
  padding-bottom: 277px;
}
#card2{
  position:fixed;
  left :0;
  padding-top: 20px;
  font-size : 20px;
  text-align: left;
}
#card3{
   position: fixed;
   right :0;
   padding-top:0px;
}
#card4{
   position: fixed;
   left :100px;
   right : 100px;

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
</style>
