
class RequestDataService:

    def getRequestsByFilter(self):
        """Get requests by filter"""
        with getSession() as session:
            statusList=self.sortStatusArea.grabCheckedList()
            teamList=self.sortTeamArea.grabCheckedList()
            effortList=self.sortEffortArea.grabCheckedList()
            requestTypeList=self.sortRequestTypesArea.grabCheckedList()
            businessUnitList=self.businessUnitArea.grabCheckedList()
            query = (session.query(
                Request.group_id,
                func.count().label('CT')
            )
            .group_by(Request.group_id)
            )