
import asyncio

async def recive():
    await asyncio.sleep(2)
    return "smt smt message"

async def dashboard_get():
    await asyncio.sleep(6)
    return "dashboard"

# TODO: implement
def dashbaord_channel_active(socket_id: int) -> bool:
    if socket_id == 1:
        return True

    return False

def build_tasks(socket_id: int) -> list[asyncio.Task]:
    tasks = []
    
    
    if dashbaord_channel_active(socket_id):
        tasks.append(asyncio.create_task(dashboard_get()))
    
    

    return tasks



# TODO: add logic to check if dashboard channel is active - if not dont run dashboard_get()
async def main(socket_id: int = 1):
    """
    Runs two coroutines - recive() and dashboard_get() - concurrently using asyncio.wait().
    Only one of the two coroutines are completed. The first one to finish is the one to controll the flow.
    1. recive() awaits messages from a socket and returns either subscription updates or dashboard filters.
        If this function is executed the subscriptions or dashboard filters are alterd 
    
    dashboard_get() gets the dashboard and sleeps for 6 seconds before executing.
    

    Args:
    Returns:
        None: No value is returned from this function.

    Raises:
        Any exceptions raised by recive() or dashboard_get() are propagated to the caller.

    Example:
        ```
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        ```
    """
    tasks: list[asyncio.Task] = build_tasks(socket_id)
    
    # TODO: move this to build_tasks use socket.recive_json()
    tasks.append(asyncio.create_task(recive()))
    
    done, running = await asyncio.wait(
            tasks,
            timeout=20,
            return_when = asyncio.FIRST_COMPLETED
        )
    
    done = done.pop()
    running = running.pop()
    
    # get the result of the completed task and cancel the running one
    print(done.result(), running.cancel())
    
    # now we need to decide the further flow
    print("getting coro")
    if done.get_coro().__name__ == 'dashboard_get':
        print("done")
        return
    
    # TODO: update subscriptions 
    # return
    
    # TODO: update filters
    # musst not forget to return new dashboard data
    # await dashboard_get() 
    
    
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())