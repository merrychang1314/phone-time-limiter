# -*- coding: utf-8 -*-
"""
手机时间限制器 - 修复版本
简化版本，减少可能的错误点
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from datetime import datetime, timedelta

class PhoneTimeLimiterApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limit_active = False
        self.end_time = None
        self.password = "1234"
        
    def build(self):
        self.title = "手机时间限制器"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text='手机时间限制器',
            font_size='24sp',
            size_hint_y=None,
            height='60dp'
        )
        layout.add_widget(title)
        
        # 状态显示
        self.status_label = Label(
            text='当前状态：未激活限制',
            font_size='16sp',
            size_hint_y=None,
            height='40dp'
        )
        layout.add_widget(self.status_label)
        
        # 时间输入
        time_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        time_layout.add_widget(Label(text='限制时长(分钟):', size_hint_x=0.4))
        self.time_input = TextInput(
            text='30',
            multiline=False,
            input_filter='int',
            size_hint_x=0.6
        )
        time_layout.add_widget(self.time_input)
        layout.add_widget(time_layout)
        
        # 密码输入
        pwd_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        pwd_layout.add_widget(Label(text='解锁密码:', size_hint_x=0.4))
        self.password_input = TextInput(
            text=self.password,
            multiline=False,
            password=True,
            size_hint_x=0.6
        )
        pwd_layout.add_widget(self.password_input)
        layout.add_widget(pwd_layout)
        
        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing=10)
        
        self.start_button = Button(text='开始限制')
        self.start_button.bind(on_press=self.start_limit)
        btn_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='解除限制', disabled=True)
        self.stop_button.bind(on_press=self.stop_limit)
        btn_layout.add_widget(self.stop_button)
        
        layout.add_widget(btn_layout)
        
        # 紧急呼叫
        emergency_btn = Button(
            text='紧急呼叫',
            size_hint_y=None,
            height='60dp'
        )
        emergency_btn.bind(on_press=self.emergency_call)
        layout.add_widget(emergency_btn)
        
        # 倒计时
        self.countdown_label = Label(
            text='',
            font_size='18sp',
            size_hint_y=None,
            height='40dp'
        )
        layout.add_widget(self.countdown_label)
        
        # 说明
        info_label = Label(
            text='使用说明：设置时长和密码后点击开始限制',
            font_size='12sp',
            size_hint_y=None,
            height='30dp'
        )
        layout.add_widget(info_label)
        
        return layout
    
    def start_limit(self, instance):
        """开始限制"""
        try:
            minutes = int(self.time_input.text)
            if minutes <= 0:
                return
                
            self.password = self.password_input.text
            self.end_time = datetime.now() + timedelta(minutes=minutes)
            self.limit_active = True
            
            # 更新UI状态
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.time_input.disabled = True
            self.password_input.disabled = True
            
            self.status_label.text = f'限制已激活，将于 {self.end_time.strftime("%H:%M:%S")} 结束'
            
            # 开始倒计时
            Clock.schedule_interval(self.update_countdown, 1)
            
        except ValueError:
            self.status_label.text = '错误：请输入有效的数字'
    
    def update_countdown(self, dt):
        """更新倒计时"""
        if not self.limit_active or not self.end_time:
            return False
            
        now = datetime.now()
        if now >= self.end_time:
            self.stop_limit_internal()
            return False
            
        remaining = self.end_time - now
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        self.countdown_label.text = f'剩余时间: {hours:02d}:{minutes:02d}:{seconds:02d}'
        return True
    
    def stop_limit(self, instance):
        """解除限制（简化版本）"""
        self.stop_limit_internal()
    
    def stop_limit_internal(self):
        """内部解除限制方法"""
        self.limit_active = False
        self.end_time = None
        
        # 恢复UI状态
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.time_input.disabled = False
        self.password_input.disabled = False
        
        self.status_label.text = '当前状态：未激活限制'
        self.countdown_label.text = ''
        
        Clock.unschedule(self.update_countdown)
    
    def emergency_call(self, instance):
        """紧急呼叫功能"""
        self.status_label.text = '紧急呼叫功能（在真实Android环境中可用）'

if __name__ == '__main__':
    PhoneTimeLimiterApp().run()
