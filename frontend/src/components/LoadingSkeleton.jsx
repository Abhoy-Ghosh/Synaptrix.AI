const LoadingSkeleton = () => {

  return (

    <div className="mt-16 space-y-10 animate-pulse">

      {/* SUMMARY */}

      <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8">

        <div className="h-10 w-64 bg-zinc-700 rounded mb-8" />

        <div className="space-y-4">

          <div className="h-5 bg-zinc-700 rounded w-full" />
          <div className="h-5 bg-zinc-700 rounded w-full" />
          <div className="h-5 bg-zinc-700 rounded w-5/6" />
          <div className="h-5 bg-zinc-700 rounded w-4/6" />

        </div>

      </div>

      {/* PAPER CARDS */}

      <div className="grid xl:grid-cols-2 gap-10">

        {[1,2,3,4].map((item)=>(

          <div
            key={item}
            className="bg-[#111827] border border-zinc-800 rounded-3xl p-8"
          >

            <div className="h-8 bg-zinc-700 rounded w-4/5 mb-6" />

            <div className="h-4 bg-zinc-700 rounded w-32 mb-8" />

            <div className="space-y-4">

              <div className="h-4 bg-zinc-700 rounded w-full" />
              <div className="h-4 bg-zinc-700 rounded w-full" />
              <div className="h-4 bg-zinc-700 rounded w-5/6" />

            </div>

          </div>

        ))}

      </div>

    </div>

  )
}

export default LoadingSkeleton