class Report:
    def __init__(self, reportNo, channelNo):
        self.reportNo = reportNo
        self.channelNo = channelNo

    def __str__(self):
        return "reportNo:{}, channelNo:{}".format(self.reportNo, self.channelNo)

    def __eq__(self, other) -> bool:
        return self.reportNo == other.reportNo

    def __hash__(self):
        return hash(self.reportNo)

    def setCustomer(self, customer):
        self.customer = customer

    def setProject(self, project):
        self.project = project


class Customer:
    def __init__(self, Id, tel, name, sex):
        self.Id = Id
        self.tel = tel
        self.name = name
        self.sex = sex
        self.desc = ''
        # self.intentions = []

    def setDesc(self, desc):
        self.desc = desc

    # def addIntentions(self, project):
    #     self.intentions.append(project)

    def __str__(self):
        return "Id:{},name:{},tel:{},sex:{},desc:{}".format(self.Id, self.name, self.tel, self.sex, self.desc)

    def __eq__(self, other) -> bool:
        return self.Id == other.Id

    def __hash__(self):
        return hash(self.Id)


class BuildingProject:
    def __init__(self, projectId, name):
        self.projectId = projectId
        self.name = name

    def __str__(self):
        return "projectId:{},name:{}".format(self.projectId, self.name)

    def __eq__(self, other) -> bool:
        return self.projectId == other.projectId

    def __hash__(self):
        return hash(self.projectId)


if __name__ == '__main__':
    itemNo = 'BAOBEI1001'
    channelNo = 'WFQD1001'
    report = Report(itemNo, channelNo)

    userId = '1001'
    userName = '陈先生'
    tel = '13518833380'
    sex = 1
    desc = '购房需求'
    customer = Customer(userId, tel, userName, sex)
    customer.setDesc(desc)

    projectId = '110210'
    projectName = '雅居乐金沙湾'
    project = BuildingProject(projectId, projectName)

    report.setCustomer(customer)
    report.setProject(project)

    print('worker({}) report参数({})'.format(userId, report))
    print('worker(%s) customer参数(%s)' % userId % customer)
    print(f'worker(%s) project参数(%s)' % userId % project)