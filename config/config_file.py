# 钉钉机器人相关配置

# 钉钉机器人webhook：webhook + access_token
dd_robot_webhook = r"https://oapi.dingtalk.com/robot/send"
dd_robot_access_token = {"access_token": "?"}

# 调用钉钉机器人headers定义
dd_robot_headers = {'Content-Type': 'application/json'}

# 钉钉机器人加签数据定义
dd_secret = '?'



# testcase_excel格式定义，不能更改
xlsx_format = ("name", "method", "api", "params", "json_data", "x_www_form_urlencoded_data")

# env_excel格式定义，不能更改
env_xlsx_format = ("project_name", "test_env", "real_env")

