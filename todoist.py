from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import os
import pendulum

#load_dotenv()
#TODOIST_API = os.environ.get('TODOIST_API', '')

def make_todoist(todoist_api):
    try:
        message = ""
        api = TodoistAPI(todoist_api)
        tasks_today = api.get_tasks(filter = 'overdue | due:today')
        count_today = len(tasks_today)
        message += f'今日待办事项共{count_today}项。'

        tasks_p1 = api.get_tasks(filter = '(overdue | due:today) & p1')
        count_p1 = len(tasks_p1)
        if count_p1 > 0:
            message_p1 = "\r\nP1 优先级的任务有: "
            for task in tasks_p1:
                message_p1 += f'\r\n- {task.content}'
            message += message_p1
        else:
            message += "\r\n没有 P1 优先级的任务..."

        tasks_p2 = api.get_tasks(filter = '(overdue | due:today) & p2')
        count_p2 = len(tasks_p2)
        if count_p2 > 0:
            message_p2 = "\r\nP2 优先级的任务有: "
            for task in tasks_p2:
                message_p2 += f'\r\n- {task.content}'
            message += message_p2
        else:
            message += "\r\n没有 P2 优先级的任务..."

        message += "\r\n\r\nPowered by Todoist.com"
        print(f'Todoist Message...')
        print(message)
        return message
    except Exception as error:
        print(error)
        return "获取Todoist数据失败..."

if __name__ == "__main__":
    print(TODOIST_API)
    make_todoist(TODOIST_API)
    