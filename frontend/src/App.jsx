import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Play, 
  Pause, 
  Settings, 
  Eye, 
  CheckCircle, 
  XCircle, 
  Clock, 
  TrendingUp, 
  Users, 
  DollarSign,
  Video,
  Image,
  FileText,
  Calendar,
  Bell,
  BarChart3,
  Zap,
  Globe,
  Smartphone
} from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [isSystemRunning, setIsSystemRunning] = useState(true)
  const [pendingPreviews, setPendingPreviews] = useState([])
  const [channels, setChannels] = useState([
    {
      id: 'horror_stories',
      name: 'قصص الرعب',
      platform: 'TikTok',
      status: 'active',
      followers: 15420,
      todayViews: 8750,
      revenue: 245.50,
      contentGenerated: 12,
      publishedToday: 3
    },
    {
      id: 'islamic_stories',
      name: 'القصص الإسلامية',
      platform: 'TikTok',
      status: 'active',
      followers: 22100,
      todayViews: 12300,
      revenue: 380.75,
      contentGenerated: 15,
      publishedToday: 4
    },
    {
      id: 'home_design',
      name: 'تصميم المنازل والعقارات',
      platform: 'YouTube',
      status: 'active',
      followers: 8900,
      todayViews: 5600,
      revenue: 195.25,
      contentGenerated: 8,
      publishedToday: 2
    },
    {
      id: 'motivation',
      name: 'التحفيز والاقتباسات',
      platform: 'TikTok',
      status: 'active',
      followers: 31500,
      todayViews: 18900,
      revenue: 520.80,
      contentGenerated: 20,
      publishedToday: 5
    },
    {
      id: 'ai_chef',
      name: 'AI Chef',
      platform: 'YouTube',
      status: 'active',
      followers: 12750,
      todayViews: 9200,
      revenue: 310.40,
      contentGenerated: 10,
      publishedToday: 3
    }
  ])

  const [systemStats, setSystemStats] = useState({
    totalViews: 54750,
    totalRevenue: 1652.70,
    totalFollowers: 90670,
    contentGenerated: 65,
    publishedToday: 17,
    pendingPreviews: 8,
    scheduledContent: 25
  })

  useEffect(() => {
    // Simulate loading pending previews
    setPendingPreviews([
      {
        id: 'preview_1',
        channelId: 'horror_stories',
        title: 'قصة الدمية المسكونة',
        content: 'في منزل قديم بالريف، وجدت سارة دمية قديمة في العلية...',
        scheduledTime: '22:00',
        timeLeft: '45 دقيقة',
        mediaType: 'video'
      },
      {
        id: 'preview_2',
        channelId: 'ai_chef',
        title: 'وصفة المعكرونة الإيطالية',
        content: 'اليوم سنتعلم طريقة عمل المعكرونة الإيطالية الأصلية...',
        scheduledTime: '22:15',
        timeLeft: '60 دقيقة',
        mediaType: 'video'
      },
      {
        id: 'preview_3',
        channelId: 'motivation',
        title: 'اقتباس عن النجاح',
        content: 'النجاح ليس نهاية الطريق، والفشل ليس نهاية العالم...',
        scheduledTime: '22:30',
        timeLeft: '75 دقيقة',
        mediaType: 'image'
      }
    ])
  }, [])

  const toggleSystem = () => {
    setIsSystemRunning(!isSystemRunning)
  }

  const approveContent = (contentId) => {
    setPendingPreviews(prev => prev.filter(item => item.id !== contentId))
    // In real app, send approval to backend
    console.log(`Approved content: ${contentId}`)
  }

  const rejectContent = (contentId) => {
    setPendingPreviews(prev => prev.filter(item => item.id !== contentId))
    // In real app, send rejection to backend
    console.log(`Rejected content: ${contentId}`)
  }

  const getChannelIcon = (platform) => {
    return platform === 'TikTok' ? <Smartphone className="h-4 w-4" /> : <Video className="h-4 w-4" />
  }

  const getMediaIcon = (mediaType) => {
    switch(mediaType) {
      case 'video': return <Video className="h-4 w-4" />
      case 'image': return <Image className="h-4 w-4" />
      default: return <FileText className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800" dir="rtl">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-100 mb-2">
              نظام أتمتة المحتوى بالذكاء الاصطناعي
            </h1>
            <p className="text-slate-600 dark:text-slate-400">
              إدارة 5 قنوات تلقائية مع معاينة المحتوى والنشر الذكي
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant={isSystemRunning ? "default" : "secondary"} className="px-4 py-2">
              <Zap className="h-4 w-4 ml-2" />
              {isSystemRunning ? 'النظام يعمل' : 'النظام متوقف'}
            </Badge>
            <Button 
              onClick={toggleSystem}
              variant={isSystemRunning ? "destructive" : "default"}
              size="lg"
            >
              {isSystemRunning ? <Pause className="h-4 w-4 ml-2" /> : <Play className="h-4 w-4 ml-2" />}
              {isSystemRunning ? 'إيقاف النظام' : 'تشغيل النظام'}
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard">لوحة التحكم</TabsTrigger>
            <TabsTrigger value="channels">القنوات</TabsTrigger>
            <TabsTrigger value="preview">معاينة المحتوى</TabsTrigger>
            <TabsTrigger value="analytics">التحليلات</TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">إجمالي المشاهدات</CardTitle>
                  <TrendingUp className="h-4 w-4" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{systemStats.totalViews.toLocaleString()}</div>
                  <p className="text-xs text-blue-100">+12% من الأمس</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">الإيرادات اليومية</CardTitle>
                  <DollarSign className="h-4 w-4" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${systemStats.totalRevenue}</div>
                  <p className="text-xs text-green-100">+8% من الأمس</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">إجمالي المتابعين</CardTitle>
                  <Users className="h-4 w-4" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{systemStats.totalFollowers.toLocaleString()}</div>
                  <p className="text-xs text-purple-100">+156 متابع جديد</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-orange-500 to-orange-600 text-white">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">المحتوى المنشور اليوم</CardTitle>
                  <FileText className="h-4 w-4" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{systemStats.publishedToday}</div>
                  <p className="text-xs text-orange-100">من أصل {systemStats.contentGenerated} مُولد</p>
                </CardContent>
              </Card>
            </div>

            {/* System Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5" />
                    حالة النظام
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>توليد المحتوى</span>
                    <Badge variant="default">نشط</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>البحث التلقائي</span>
                    <Badge variant="default">نشط</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>معاينة المحتوى</span>
                    <Badge variant="secondary">21:00 - 22:00</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>النشر التلقائي</span>
                    <Badge variant="default">بعد 22:00</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Bell className="h-5 w-5" />
                    الإشعارات الحديثة
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                    <div className="text-sm">
                      <p className="font-medium">تم نشر محتوى جديد</p>
                      <p className="text-slate-600 dark:text-slate-400">قناة قصص الرعب - منذ 5 دقائق</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                    <Clock className="h-4 w-4 text-yellow-500 mt-0.5" />
                    <div className="text-sm">
                      <p className="font-medium">محتوى في انتظار المعاينة</p>
                      <p className="text-slate-600 dark:text-slate-400">3 عناصر تحتاج مراجعة</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <TrendingUp className="h-4 w-4 text-green-500 mt-0.5" />
                    <div className="text-sm">
                      <p className="font-medium">زيادة في المشاهدات</p>
                      <p className="text-slate-600 dark:text-slate-400">قناة AI Chef +25% اليوم</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Channels Tab */}
          <TabsContent value="channels" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {channels.map((channel) => (
                <Card key={channel.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        {getChannelIcon(channel.platform)}
                        {channel.name}
                      </CardTitle>
                      <Badge variant={channel.status === 'active' ? 'default' : 'secondary'}>
                        {channel.status === 'active' ? 'نشط' : 'متوقف'}
                      </Badge>
                    </div>
                    <CardDescription>{channel.platform}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-slate-600 dark:text-slate-400">المتابعون</p>
                        <p className="font-semibold">{channel.followers.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-slate-600 dark:text-slate-400">مشاهدات اليوم</p>
                        <p className="font-semibold">{channel.todayViews.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-slate-600 dark:text-slate-400">الإيرادات</p>
                        <p className="font-semibold text-green-600">${channel.revenue}</p>
                      </div>
                      <div>
                        <p className="text-slate-600 dark:text-slate-400">منشور اليوم</p>
                        <p className="font-semibold">{channel.publishedToday}/{channel.contentGenerated}</p>
                      </div>
                    </div>
                    <Progress value={(channel.publishedToday / channel.contentGenerated) * 100} className="h-2" />
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" className="flex-1">
                        <Settings className="h-4 w-4 ml-2" />
                        إعدادات
                      </Button>
                      <Button size="sm" variant="outline" className="flex-1">
                        <BarChart3 className="h-4 w-4 ml-2" />
                        إحصائيات
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Preview Tab */}
          <TabsContent value="preview" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-5 w-5" />
                  معاينة المحتوى (21:00 - 22:00)
                </CardTitle>
                <CardDescription>
                  راجع المحتوى المُولد قبل النشر التلقائي في الساعة 22:00
                </CardDescription>
              </CardHeader>
              <CardContent>
                {pendingPreviews.length === 0 ? (
                  <div className="text-center py-8 text-slate-500 dark:text-slate-400">
                    <Eye className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>لا يوجد محتوى في انتظار المعاينة حالياً</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {pendingPreviews.map((content) => (
                      <Card key={content.id} className="border-l-4 border-l-blue-500">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-2">
                              {getMediaIcon(content.mediaType)}
                              <h3 className="font-semibold">{content.title}</h3>
                              <Badge variant="outline">
                                {channels.find(c => c.id === content.channelId)?.name}
                              </Badge>
                            </div>
                            <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                              <Clock className="h-4 w-4" />
                              {content.timeLeft}
                            </div>
                          </div>
                          <p className="text-slate-700 dark:text-slate-300 mb-4 line-clamp-2">
                            {content.content}
                          </p>
                          <div className="flex items-center justify-between">
                            <div className="text-sm text-slate-600 dark:text-slate-400">
                              مجدول للنشر في: {content.scheduledTime}
                            </div>
                            <div className="flex gap-2">
                              <Button 
                                size="sm" 
                                variant="destructive"
                                onClick={() => rejectContent(content.id)}
                              >
                                <XCircle className="h-4 w-4 ml-2" />
                                رفض
                              </Button>
                              <Button 
                                size="sm"
                                onClick={() => approveContent(content.id)}
                              >
                                <CheckCircle className="h-4 w-4 ml-2" />
                                موافقة
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>أداء القنوات اليومي</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {channels.map((channel) => (
                      <div key={channel.id} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                        <div className="flex items-center gap-3">
                          {getChannelIcon(channel.platform)}
                          <div>
                            <p className="font-medium">{channel.name}</p>
                            <p className="text-sm text-slate-600 dark:text-slate-400">{channel.platform}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">{channel.todayViews.toLocaleString()}</p>
                          <p className="text-sm text-green-600">${channel.revenue}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>إحصائيات الإنتاج</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>المحتوى المُولد اليوم</span>
                      <span className="font-semibold">{systemStats.contentGenerated}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>المحتوى المنشور</span>
                      <span className="font-semibold text-green-600">{systemStats.publishedToday}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>في انتظار المعاينة</span>
                      <span className="font-semibold text-yellow-600">{pendingPreviews.length}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>مجدول للنشر</span>
                      <span className="font-semibold text-blue-600">{systemStats.scheduledContent}</span>
                    </div>
                    <Progress 
                      value={(systemStats.publishedToday / systemStats.contentGenerated) * 100} 
                      className="h-3"
                    />
                    <p className="text-sm text-slate-600 dark:text-slate-400 text-center">
                      معدل النشر: {Math.round((systemStats.publishedToday / systemStats.contentGenerated) * 100)}%
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

