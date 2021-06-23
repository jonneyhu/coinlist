
** path: /user **
method: 
    get:  获取所有用户
        参数:
            page
            limit
    post 创建用户
        参数: 
            username 
            password 
            
** path: /user/login **
method: 
    post 登录
        参数: 
            username 
            password 
 
** path: /address **
method: 
    get  获取所有地址
        参数:
            page
            limit
    post 创建地址
        参数:
            address
            postcode
            country
     
** path: /email **
method: 
    get  获取所有邮箱
        参数:
            page
            limit
    post 创建邮箱
        参数:
            email
            password
            assist
    
** path: /proxy **
method: 
    get  获取所有代理
        参数:
            page
            limit
    post 创建代理
        参数:
            server
            origin_ip
            country
    
    
** path: /account **
method: 
    get  获取所有已提交账户
        参数:
            page
            limit
            email           邮箱 (非必须)
            use_status      使用状态(非必须,0未使用 1已使用)
            register_status 注册状态(非必须,0审核中,1注册成功,2注册失败)
            country         国家(非必须)
    post 分配账户
        参数;
            username
            accounts
    
    
** path: /available **
method: 
    get  获取可用资源
        参数:
            page
            limit
    
    
** path: /account/self **
method: 
    get  获取我的账户
        参数:
            page
            limit

    
** path: /account/make **
method: 
    get  获取我的制作中账户
        参数:
            page
            limit
    post 批量创建账户
        参数:
            amount
            country
    put  提交账户
        参数:
            email
    
** path: /account/sync **
method: 
    get  获取同步账户
