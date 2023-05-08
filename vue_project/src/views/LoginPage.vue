<!--  -->
<template>
    <div class="loginbBody">
        <div class="loginDiv">
            <div class="login-content">
                <h1 class="login-title"  style="height:auto">用户登录</h1>
                <el-form :model="loginForm" label-width="100px" :rules="rules" ref="loginForm">
                    <el-form-item label="名字" prop="name" style="height:auto">
                        <el-input style="width: 200px" type="text" v-model="loginForm.name" autocomplete="off"
                            size="small"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password" style="height:auto">
                        <el-input style="width: 200px" type="password" v-model="loginForm.password" show-password
                            autocomplete="off" size="small"></el-input>
                    </el-form-item>
                    <el-form-item  style="height:auto">
                        <el-button type="primary" @click="confirm">确 定</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import { userLogin } from "@/api/index"
export default {
    //组件名称
    name: 'LoginPage',
    //父组件传递值
    props: {
    },
    //import引入的组件需要注入到对象中才能使用
    components: {},
    data() {
        //这里存放数据
        return {
            loginForm: {
                name: '',
                password: ''
            },
            rules: {
                name: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 6, message: '用户名长度在 3 到 6 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输密码', trigger: 'blur' },
                    { min: 3, max: 6, message: '密码长度在 3 到 6 个字符', trigger: 'blur' }
                ]
            }
        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
        confirm() {
            this.$refs.loginForm.validate((valid) => {
                if (valid) { //valid成功为true，失败为false
                    userLogin({
                        user_name:this.loginForm.name,
                        password:this.loginForm.password
                    }).then(res=>{
                        if (res.return_code=="OK"){
                            window.sessionStorage.setItem("token",res.data.token)
                            this.$router.push('/home/menu1');
                        }
                    })
                    
                } else {
                    console.log('校验失败');
                    return false;
                }
            });
        }

    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() {

    },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {

    },
    beforeCreate() { }, //生命周期 - 创建之前
    beforeMount() { }, //生命周期 - 挂载之前
    beforeUpdate() { }, //生命周期 - 更新之前
    updated() { }, //生命周期 - 更新之后
    beforeDestroy() { }, //生命周期 - 销毁之前
    destroyed() { }, //生命周期 - 销毁完成
    activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
}
</script>


<style scoped >


.loginbBody {
    width: 100%;
    height: 100%;
    position: fixed;
    /* background-image: linear-gradient(to right, #ffffff, #e9e8fa, #d1d2f6, #b5bdf3, #94a9ef, #79a6f0, #55a4f0, #00a2ef, #00aeeb, #00b8e2, #00c0d5, #00c7c6); */
    background-color: #dadde3;
    
}

.loginDiv {
   
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -200px;
    margin-left: 200px;
    width: 450px;
    height: 330px;
    background: #fff;
    border-radius: 5%;


}

.login-title {
    margin: 20px 0;
    text-align: center;
}

.login-content {
    width: 400px;
    height: 250px;
    position: absolute;
    top: 25px;
    left: 25px;
}


</style>