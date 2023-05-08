<!--  -->
<template>
    <header>
        <div style="display:flex;cursor: pointer;" @click="to_home">
            <h1 style="margin-top: 0px;color: #425049;font-size:30px; ">工作流编排与可视化平台</h1>
        </div>

        <div class="menu" style="width: 50%;">
            <el-menu :default-active="current_route" ref="menu" class="el-menu-demo" mode="horizontal" router>
                <el-menu-item index="/home/menu1" style="width:16%;font-size: large;">首页</el-menu-item>
                <el-menu-item index="/home/menu2" style="width:16%;font-size: large;">编辑</el-menu-item>
                <el-menu-item index="/home/menu3" style="width:16%;font-size: large;">绘图</el-menu-item>
            </el-menu>
        </div>


        <div class="opt-wrapper">
            <el-dropdown :hide-on-click="false">
                <div class="demo-basic--circle">
                    <div class="block">
                        <el-avatar :size="40" :src="avatar" :class="['avatar-info']">
                        </el-avatar>
                    </div>
                </div>
                <el-dropdown-menu slot="dropdown" style="margin-top:0px;margin-left: 0px;height:100px">
                    <el-dropdown-item style="height:40px"><i class="el-icon-info"></i>个人中心</el-dropdown-item>
                    <el-dropdown-item style="height:40px" @click.native="logout"><i
                            class="el-icon-switch-button"></i>退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </header>

</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';


export default {
    //组件名称
    name: 'Header',
    //父组件传递值
    props: {
    },
    //import引入的组件需要注入到对象中才能使用
    components: {
        
    },
    data() {
        //这里存放数据
        return {
            avatar: require('@/assets/images/touxiang.png'),
            current_route:this.$route.path
        }
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {
        $route: {
            handler(to, from) {
                if(["/home/menu1","/home/menu2","/home/menu3"].includes(to.fullPath)){
                    this.$refs.menu.$data.activeIndex = to.fullPath
                }
            }
        }
    },
    //方法集合
    methods: {
        logout() {
            //跳转到登录路由
            this.$router.push({ path: "/login" })
        },
        to_home() {
            if (this.$route.path != "/home/menu1") {
                this.$router.push({ path: "/home/menu1" })
            }
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
<style scoped>
/**scoped 表示样式只在当前组件有效*/

header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #fff;
    height: 100%
}

/*设定头像图片样式*/
.avatar-info {
    margin-top: 20px;
    margin-right: 40px;
    cursor: pointer;
}
</style>